import streamlit as st
import pandas as pd
import json

# Sample Data for deposits and user wallets
deposits_data = [
    {'username': 'PoEconomics', 'date': '18th May', 'deposit': 18.5},
    {'username': 'JESUS', 'date': '18th May', 'deposit': 9.88},
    {'username': 'eepee', 'date': '18th May', 'deposit': 10},
    {'username': 'ElVincenzo', 'date': '18th May', 'deposit': 33.45},
    # Add more data as needed
]

# Admin credentials
ADMIN_USERNAME = 'Admin'
ADMIN_PASSWORD = 'AdminPOEconomics'

# Store all wallets and deposits
wallets = {}

# Helper functions
def login():
    """Handle Admin login."""
    with st.form(key='login_form'):
        st.text_input('Username', key='admin_username')
        st.text_input('Password', type='password', key='admin_password')
        login_button = st.form_submit_button("Login")
        
        if login_button:
            if st.session_state.admin_username == ADMIN_USERNAME and st.session_state.admin_password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.wallets = wallets
                st.success("Login successful!")
                return True
            else:
                st.error("Invalid credentials, try again!")
                return False
    return False

# Display admin login page
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    if not login():
        st.stop()

# If logged in, show wallet information and allow management
if st.session_state.logged_in:
    st.title("FundBank - Admin Dashboard")
    st.subheader("Manage Deposits & View Wallets")

    # Option to add new deposit
    st.header("Add New Deposit")
    deposit_username = st.text_input('Username of the depositor')
    deposit_amount = st.number_input('Deposit Amount (Divines)', min_value=0.0, step=0.01)
    deposit_date = st.date_input("Deposit Date")
    
    if st.button('Add Deposit'):
        if deposit_username and deposit_amount > 0:
            new_deposit = {
                'username': deposit_username,
                'date': deposit_date.strftime('%d %B'),
                'deposit': deposit_amount
            }
            deposits_data.append(new_deposit)
            st.success(f"Deposit of {deposit_amount} Divines added for {deposit_username}.")
        else:
            st.error("Please fill all the fields correctly.")

    # Display the total balance of all wallets
    st.header("Total Wallets Balance")
    total_balance = sum(deposit['deposit'] for deposit in deposits_data)
    st.write(f"Total Fund Value: {total_balance} Divines")

    # Display all wallet balances
    st.header("All Wallets")
    user_wallets = {}
    for data in deposits_data:
        if data['username'] not in user_wallets:
            user_wallets[data['username']] = 0
        user_wallets[data['username']] += data['deposit']
    
    # Display a table of all users with total balance
    df_wallets = pd.DataFrame(user_wallets.items(), columns=["Username", "Total Balance"])
    st.dataframe(df_wallets)

    # Option to search for a specific user's wallet
    search_username = st.text_input('Search for Wallet by Username')
    if search_username:
        user_wallet = {k: v for k, v in user_wallets.items() if k.lower() == search_username.lower()}
        if user_wallet:
            st.write(f"Wallet for {search_username}:")
            st.write(f"Total Balance: {list(user_wallet.values())[0]} Divines")
        else:
            st.warning(f"No wallet found for username: {search_username}")

    # Allow the admin to set the daily percentage growth
    st.header("Set Daily Percentage Growth")
    percentage_growth = st.number_input('Growth Percentage for Next Day (%)', min_value=0.0, max_value=100.0, step=0.0001)
    
    if st.button("Set Growth Percentage"):
        st.session_state.percentage_growth = percentage_growth
        st.success(f"Growth percentage set to {percentage_growth}% for the next day.")

    # Display all data
    st.header("Deposit History")
    df_deposits = pd.DataFrame(deposits_data)
    st.write(df_deposits)

    # Option to logout
    if st.button('Logout'):
        st.session_state.logged_in = False
        st.experimental_rerun()
