import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adminpass"

# Initialize session state
if 'user_deposits' not in st.session_state:
    st.session_state.user_deposits = {}
if 'growth_percentage' not in st.session_state:
    st.session_state.growth_percentage = {}

# Sample initial data for user deposits (to simulate the bank's records)
if 'deposits_data' not in st.session_state:
    st.session_state.deposits_data = pd.DataFrame(columns=['Username', 'Date', 'Deposit'])

# Function to authenticate admin
def admin_login():
    st.title("FundBank Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.session_state.is_admin_authenticated = True
        st.success("Logged in as Admin!")
    else:
        st.session_state.is_admin_authenticated = False
        st.warning("Invalid credentials")

# Function to handle user deposit tracking
def user_deposit_page():
    st.title("FundBank - User Deposit Tracker")
    
    # Get today's date for deposit tracking
    today = datetime.today().strftime('%Y-%m-%d')
    user_name = st.text_input("Enter your username:")
    
    if user_name:
        user_deposit = 0
        user_growth = 0
        if user_name in st.session_state.user_deposits:
            user_deposit = st.session_state.user_deposits[user_name].get(today, 0)
            user_growth = st.session_state.growth_percentage.get(today, 0)

        st.write(f"Your deposit for today: {user_deposit} units")
        st.write(f"Your deposit growth today: {user_growth}%")
        
        # Display the current balance and growth over time for this user
        if user_name in st.session_state.user_deposits:
            user_data = pd.DataFrame.from_dict(st.session_state.user_deposits[user_name], orient='index', columns=['Deposit'])
            user_data.index.name = 'Date'
            st.dataframe(user_data)
        
        # Option to add a deposit (For the user)
        new_deposit = st.number_input("Deposit for today (Units):", min_value=0)
        if st.button("Submit Deposit"):
            if user_name not in st.session_state.user_deposits:
                st.session_state.user_deposits[user_name] = {}
            st.session_state.user_deposits[user_name][today] = new_deposit
            st.success(f"Deposit of {new_deposit} units added successfully for {user_name}!")

# Admin controls to set the growth percentage each day
def admin_controls():
    st.title("Admin Controls")

    # Set growth percentage for the day
    growth_percentage = st.number_input("Set the growth percentage for today:", min_value=0, max_value=100)
    today = datetime.today().strftime('%Y-%m-%d')

    if st.button("Set Growth Percentage"):
        st.session_state.growth_percentage[today] = growth_percentage
        st.success(f"Growth percentage for {today} set to {growth_percentage}%")

    # Display the current growth percentages for the past days
    st.write("Growth percentages for the past days:")
    growth_data = pd.DataFrame(list(st.session_state.growth_percentage.items()), columns=["Date", "Growth Percentage"])
    st.dataframe(growth_data)

# Main function to display different pages for users and admins
def main():
    if 'is_admin_authenticated' not in st.session_state:
        st.session_state.is_admin_authenticated = False

    page = st.sidebar.selectbox("Select a Page", ["User Deposit Tracker", "Admin Controls"])

    if page == "User Deposit Tracker":
        user_deposit_page()
    elif page == "Admin Controls":
        if st.session_state.is_admin_authenticated:
            admin_controls()
        else:
            admin_login()

if __name__ == "__main__":
    main()
