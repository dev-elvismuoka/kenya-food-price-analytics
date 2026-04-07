import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

# 1. Open the vault for the database password
load_dotenv()
db_url = os.getenv("DATABASE_URL")

print("Downloading real market data for Maize and Beans...")

try:
    # 2. The official live URL for Kenya Food Prices (Humanitarian Data Exchange)
    csv_url = "https://data.humdata.org/dataset/e0d3fba6-f9a2-45d7-b949-140c455197ff/resource/517ee1bf-2437-4f8c-aa1b-cb9925b9d437/download/wfp_food_prices_ken.csv"
    
    # Read the data, skipping the weird formatting row (row 1)
    df = pd.read_csv(csv_url, skiprows=[1])
    
    # 3. Filter strictly for Maize and Beans
    items = ['maize', 'beans']
    pattern = '|'.join(items)
    
    # Keep only the rows where the commodity is maize or beans
    real_data = df[df['commodity'].str.contains(pattern, case=False, na=False)].copy()
    
    # Clean it up: Drop empty prices and just grab the latest 1,000 records to keep it fast
    latest_data = real_data[['date', 'market', 'commodity', 'price']].dropna().tail(1000)
    
    print(f" Found the data! Pushing {len(latest_data)} records to Neon...")

    # 4. Connect to your Neon database
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO raw_food_prices (date, market_name, commodity_name, price)
    VALUES (%s, %s, %s, %s)
    """
    
    # 5. Push the data row by row
    for index, row in latest_data.iterrows():
        cursor.execute(insert_query, (row['date'], row['market'], row['commodity'], row['price']))
        
    # Save the changes
    conn.commit()
    cursor.close()
    conn.close()
    
    print(" Maize and Beans data successfully saved to your database!")

except Exception as e:
    print(f" Error: {e}")