import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Admin Credentials
ADMIN_USERNAME = 'Admin'
ADMIN_PASSWORD = 'AdminPOEconomics'

# Initialize session state for authentication and deposits
if 'admin_authenticated' not in st.session_state:
    st.session_state['admin_authenticated'] = False
if 'deposits_data' not in st.session_state:
    st.session_state['deposits_data'] = {}
if 'growth_data' not in st.session_state:
    st.session_state['growth_data'] = {}

# Function to calculate the growth for each deposit using the specific day growth rate
def calculate_growth(deposits_data, growth_data):
    growth_data_final = {}
    for user, deposits in deposits_data.items():
        user_growth = []
        total_balance = 0
        for deposit_date, deposit in sorted(deposits.items()):
            # Check the growth rate for the day
            next_day = deposit_date + timedelta(days=1)
            growth_rate = growth_data.get(deposit_date, 0)
            
            # Calculate balance
            balance = deposit * (1 + growth_rate)
            user_growth.append((deposit_date, deposit, balance))
            total_balance += balance

        growth_data_final[user] = {
            'deposits': user_growth,
            'total_balance': total_balance
        }
    return growth_data_final

# Function for Admin to login
def admin_login():
    st.title("Admin Login")
    username = st.text_input("Username", value="Admin")  # Make username visible
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state['admin_authenticated'] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

# Admin can add new deposits for users
def add_new_deposit():
    if st.session_state.get('admin_authenticated', False):
        st.title("Add New Deposit")
        username = st.text_input("Enter username to add deposit for:")
        deposit_amount = st.number_input("Enter deposit amount:", min_value=0)
        deposit_date = st.date_input("Select the date of the deposit:", min_value=datetime(2025, 5, 18))

        if st.button("Add Deposit"):
            if username and deposit_amount > 0:
                deposit_date = datetime.strptime(str(deposit_date), "%Y-%m-%d")
                if username not in st.session_state['deposits_data']:
                    st.session_state['deposits_data'][username] = {}
                st.session_state['deposits_data'][username][deposit_date] = deposit_amount
                st.success(f"Deposit of {deposit_amount} added for {username} on {deposit_date}")

# Set growth rate for each day-to-day transition
def set_daily_growth_rate():
    if st.session_state.get('admin_authenticated', False):
        st.title("Set Daily Growth Rates")
        st.write("Please enter the growth rate for each day-to-day transition. (In percentage form e.g., 5% as 0.05)")
        
        growth_rates = {}
        days = [("18th May to 19th May", "2025-05-18"), 
                ("19th May to 20th May", "2025-05-19"), 
                ("20th May to 21st May", "2025-05-20"), 
                ("21st May to 22nd May", "2025-05-21"), 
                ("22nd May to 23rd May", "2025-05-22")]

        # Loop through the days and get input for each growth rate
        for day_label, day in days:
            growth_rate = st.number_input(f"Growth rate for {day_label} (up to 4 decimals):", min_value=0.0, step=0.0001, format="%.4f")
            growth_rates[datetime.strptime(day, "%Y-%m-%d")] = growth_rate

        if st.button("Set Growth Rates"):
            st.session_state['growth_data'] = growth_rates
            st.success("Growth rates set successfully!")

# Display all user wallets and growth data
def display_user_data():
    if st.session_state.get('admin_authenticated', False):
        st.title("Users' Deposit Data and Growth")
        growth_data_final = calculate_growth(st.session_state['deposits_data'], st.session_state['growth_data'])
        
        # Display user data for all users
        if growth_data_final:
            st.write("All User Wallets:")
            for user, data in growth_data_final.items():
                st.subheader(f"User: {user}")
                st.write(f"Total Balance: {data['total_balance']} Divines")
                st.write("Deposits and Growth History:")
                for deposit_date, deposit, balance in data['deposits']:
                    st.write(f"Date: {deposit_date.strftime('%Y-%m-%d')} | Deposit: {deposit} | Balance: {balance}")
        else:
            st.write("No data available.")

# User wallet search and display
def search_wallet():
    st.title("Search User Wallet")
    user_to_search = st.text_input("Enter your username to search for your wallet:")

    if user_to_search:
        if user_to_search in st.session_state['deposits_data']:
            user_data = st.session_state['deposits_data'][user_to_search]
            growth_data_final = calculate_growth(st.session_state['deposits_data'], st.session_state['growth_data'])
            user_growth = growth_data_final.get(user_to_search, {})
            
            st.write(f"Total Balance for {user_to_search}: {user_growth['total_balance']} Divines")
            st.write("Deposits and Growth History:")
            for deposit_date, deposit, balance in user_growth['deposits']:
                st.write(f"Date: {deposit_date.strftime('%Y-%m-%d')} | Deposit: {deposit} | Balance: {balance}")
        else:
            st.write("No data found for this user.")

# Main app
def main():
    if not st.session_state.get('admin_authenticated', False):
        admin_login()
    else:
        menu = ["Add Deposit", "Set Growth Rates", "View User Data", "Search User Wallet"]
        choice = st.sidebar.selectbox("Select Option", menu)

        if choice == "Add Deposit":
            add_new_deposit()
        elif choice == "Set Growth Rates":
            set_daily_growth_rate()
        elif choice == "View User Data":
            display_user_data()
        elif choice == "Search User Wallet":
            search_wallet()

if __name__ == "__main__":
    main()
