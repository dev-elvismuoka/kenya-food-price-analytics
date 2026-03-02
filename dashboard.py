import streamlit as st
import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv

# 1. Setup and Page Config
load_dotenv()
st.set_page_config(page_title="Kenya Food Price Tracker", layout="wide")

st.title("🌽 Kenya Food Price Analytics")
st.markdown("Real-time price tracking for Maize and Beans across Kenyan markets.")

# 2. Database Connection
def get_data():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    query = "SELECT * FROM dim_food_prices ORDER BY price_date DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 3. Load and Display Data
# 3. Load and Display Data
try:
    df = get_data()
    
    # Simple Metrics at the top
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Records Tracked", len(df))
    with col2:
        st.metric("Unique Markets", df['market_location'].nunique())

    # --- NEW: Trend Analysis Chart ---
    st.subheader("📈 Price Trends Over Time")
    
    # Filter by Market
    available_markets = sorted(df['market_location'].unique())
    selected_market = st.selectbox("Select a Market to Analyze", available_markets)
    
    filtered_df = df[df['market_location'] == selected_market]
    
    # Display the Chart
    st.line_chart(
        data=filtered_df,
        x='price_date',
        y='price_kes',
        color='commodity'
    )
    # --------------------------------

    # The Data Table (Moved to bottom)
    st.subheader("Recent Cleaned Price Data")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Could not connect to database: {e}")

except Exception as e:
    st.error(f"Could not connect to database: {e}")