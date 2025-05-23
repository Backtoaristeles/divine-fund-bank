import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Starting with a mockup for FundBank system

# Admin credentials (hardcoded for simplicity)
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "AdminPOEconomics"

# Sample data for deposits, typically this would come from a database or file
# This will simulate deposit data for the users
deposits_data = {
    "username": ["user1", "user2", "user1", "user3"],
    "deposit_amount": [1000, 500, 2000, 1500],
    "date": [
        "2025-05-18", 
        "2025-05-19", 
        "2025-05-20", 
        "2025-05-21"
    ]
}

# Function to calculate the percentage growth
def calculate_growth(initial_amount, current_amount):
    return ((current_amount - initial_amount) / initial_amount) * 100

# Streamlit app structure
st.title("FundBank - Deposit Tracking")

# Admin login
st.subheader("Admin Login")

# Admin login logic
admin_username = st.text_input("Username", type="default")
admin_password = st.text_input("Password", type="password")

if admin_username == ADMIN_USERNAME and admin_password == ADMIN_PASSWORD:
    st.success("Logged in as Admin")
    
    # Get deposit details from simulated data
    df = pd.DataFrame(deposits_data)
    
    # Add a date column that will be used for growth calculation (example starts on May 18th)
    df['date'] = pd.to_datetime(df['date'])
    
    # Set up the starting date for the bank
    start_date = datetime(2025, 5, 18)
    
    # Show the deposit table
    st.subheader("Deposit History")
    st.dataframe(df)
    
    # Search for user wallet
    st.subheader("Search for Your Wallet")
    username_input = st.text_input("Enter your username")
    
    if username_input:
        user_data = df[df['username'] == username_input]
        
        if not user_data.empty:
            st.write(f"Showing data for {username_input}")
            
            # Calculate daily growth for the user
            user_deposits = user_data.sort_values(by="date")
            initial_amount = user_deposits.iloc[0]['deposit_amount']
            
            # Calculate growth for each day
            growth_values = []
            for index, row in user_deposits.iterrows():
                growth = calculate_growth(initial_amount, row['deposit_amount'])
                growth_values.append(growth)
            
            user_deposits['growth_percentage'] = growth_values
            
            # Show the user deposit details with growth
            st.dataframe(user_deposits[['date', 'deposit_amount', 'growth_percentage']])
        else:
            st.write("No data found for this username.")
    
    # Set the percentage growth for each day (admin functionality)
    st.subheader("Admin: Set Daily Growth Percentage")
    
    growth_percentage = st.number_input("Enter Growth Percentage", min_value=0, max_value=100, value=5)
    
    if st.button("Set Growth"):
        st.write(f"Daily growth set to {growth_percentage}%")

else:
    st.warning("Invalid username or password")

