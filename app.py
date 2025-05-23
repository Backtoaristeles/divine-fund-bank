import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta

# Admin Credentials
ADMIN_USERNAME = 'Admin'
ADMIN_PASSWORD = 'AdminPOEconomics'

# Set initial date for tracking (May 18th)
START_DATE = datetime(2025, 5, 18)

# User Deposit Data (this will usually be fetched from a database, for now using hardcoded data)
# Example structure: {user_name: {date: deposit_amount}}
deposits_data = {
    'PoEconomics': {
        datetime(2025, 5, 18): 50,
        datetime(2025, 5, 19): 20,
        datetime(2025, 5, 20): 10,
    },
    'JESUS': {
        datetime(2025, 5, 18): 10,
        datetime(2025, 5, 19): 5,
    }
}

# Function to calculate the growth of each deposit based on a percentage
def calculate_growth(user_deposits, daily_growth_percentage):
    growth_data = []
    previous_balance = 0

    for date, deposit in sorted(user_deposits.items()):
        # If it's the first deposit, no growth is applied
        if previous_balance == 0:
            balance = deposit
        else:
            # Apply daily growth to previous balance
            balance = previous_balance * (1 + daily_growth_percentage) + deposit
        growth_data.append((date, balance))
        previous_balance = balance
    
    return growth_data

# Set daily growth percentage (Admin Only)
def set_daily_growth():
    if st.session_state.get('admin_authenticated', False):
        daily_growth = st.number_input("Set daily growth percentage", min_value=0.0, step=0.1, value=0.02)
        return daily_growth
    else:
        st.warning("You need to be logged in as an admin to set the growth.")
        return None

# Admin login functionality
def admin_login():
    st.title("Admin Login")
    username = st.text_input("Username", type="password")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state['admin_authenticated'] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

# Main application logic
def main():
    # Authenticate Admin
    if 'admin_authenticated' not in st.session_state:
        st.session_state['admin_authenticated'] = False

    if not st.session_state['admin_authenticated']:
        admin_login()
        return
    
    # Set Daily Growth
    daily_growth = set_daily_growth()

    # If daily growth percentage is set, calculate growth for all users
    if daily_growth is not None:
        all_growth_data = {}
        for user, user_deposits in deposits_data.items():
            user_growth_data = calculate_growth(user_deposits, daily_growth)
            all_growth_data[user] = user_growth_data
        
        # Display user growth data
        st.subheader("User Wallets and Growth")
        for user, growth_data in all_growth_data.items():
            st.write(f"### {user}")
            df = pd.DataFrame(growth_data, columns=['Date', 'Balance'])
            st.write(df)

if __name__ == "__main__":
    main()
