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

# Function to calculate the growth for each deposit
def calculate_growth(deposits_data, growth_percentage):
    # Prepare a list of deposits with their growth
    growth_data = {}
    for user, deposits in deposits_data.items():
        user_growth = []
        total_balance = 0
        for date, deposit in sorted(deposits.items()):
            days_since_deposit = (datetime.today() - date).days
            balance = deposit * (1 + growth_percentage) ** days_since_deposit
            user_growth.append((date, deposit, balance))
            total_balance += balance
        growth_data[user] = {
            'deposits': user_growth,
            'total_balance': total_balance
        }
    return growth_data

# Function for Admin to login
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

# Set the daily growth rate (admin tool)
def set_growth_rate():
    if st.session_state.get('admin_authenticated', False):
        st.title("Set Growth Rate")
        growth_rate = st.number_input("Enter daily growth rate (as percentage):", min_value=0.0, max_value=100.0)
        growth_rate /= 100  # Convert percentage to decimal
        
        if st.button("Set Growth Rate"):
            st.session_state['growth_rate'] = growth_rate
            st.success(f"Daily growth rate set to {growth_rate * 100}%")

# User view for deposits and growth
def user_view():
    st.title("User View")
    username = st.text_input("Enter your username to see your deposit history:")

    if username in st.session_state['deposits_data']:
        st.write(f"Deposits for {username}:")
        growth_percentage = st.session_state.get('growth_rate', 0)  # Default to 0 if not set
        growth_data = calculate_growth(st.session_state['deposits_data'], growth_percentage)

        if username in growth_data:
            total_balance = growth_data[username]['total_balance']
            st.write(f"Your total withdrawable balance is: {total_balance:.2f} Divines")
            st.write("Deposit Growth Per Day:")
            df = pd.DataFrame(growth_data[username]['deposits'], columns=['Date', 'Deposit', 'Balance'])
            st.dataframe(df)
    else:
        st.write("No deposits found for this user.")

# Main logic: Show login, admin functions or user functions
def main():
    if st.session_state['admin_authenticated']:
        # Admin has logged in
        add_new_deposit()
        set_growth_rate()
    else:
        # Display login or user functions
        admin_login()
        user_view()

if __name__ == "__main__":
    main()
