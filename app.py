import pandas as pd
from datetime import datetime
import streamlit as st

# Example deposits data (this would normally come from user input or a database)
deposits_data = {
    "username": ["PoEconomics", "JESUS", "Chris", "Biscuit Roger", "Lord", "Alex13"],
    "deposit_amount": [100, 50, 200, 25, 5, 120],
    "date": ["2023-05-18", "2023-05-18", "2023-05-19", "2023-05-19", "2023-05-20", "2023-05-20"]
}

# Ensure that all lists have the same length, if not, add None (or a placeholder value)
max_len = max(len(deposits_data["username"]), len(deposits_data["deposit_amount"]), len(deposits_data["date"]))

# Pad shorter lists with None (or any other placeholder value you want to use)
deposits_data["username"].extend([None] * (max_len - len(deposits_data["username"])))
deposits_data["deposit_amount"].extend([None] * (max_len - len(deposits_data["deposit_amount"])))
deposits_data["date"].extend([None] * (max_len - len(deposits_data["date"])))

# Check if the lengths of all lists match
if len(deposits_data["username"]) == len(deposits_data["deposit_amount"]) == len(deposits_data["date"]):
    df = pd.DataFrame(deposits_data)
else:
    print("Data columns have mismatched lengths!")

# Display the dataframe in Streamlit
st.write("Deposits Data:")
st.write(df)

# Assuming the starting deposit for each user is already set up
starting_balance = {
    "PoEconomics": 100,  # example
    "JESUS": 50,
    "Chris": 200,
    "Biscuit Roger": 25,
    "Lord": 5,
    "Alex13": 120
}

# Function to calculate percentage growth
def calculate_growth(previous_amount, current_amount):
    if previous_amount == 0:
        return 0  # Avoid division by zero
    growth = ((current_amount - previous_amount) / previous_amount) * 100
    return growth

# Add the growth percentage column
growth_percentages = []

# Assume we have some history to compare the growth (for simplicity, using the same data here)
for index, row in df.iterrows():
    username = row["username"]
    if username in starting_balance:
        previous_balance = starting_balance[username]  # Starting balance for comparison
        current_balance = row["deposit_amount"]
        growth = calculate_growth(previous_balance, current_balance)
        growth_percentages.append(growth)
    else:
        growth_percentages.append(None)  # If no starting balance, no growth

df["growth_percentage"] = growth_percentages

# Display the dataframe with growth percentages in Streamlit
st.write("Deposits Data with Growth Percentage:")
st.write(df)

# Admin functionality to set a new percentage and update future deposits

def set_new_growth_percentage(user, new_growth_percentage):
    """
    Updates the starting balance with a new percentage growth for the user.
    """
    if user in starting_balance:
        # Update the balance based on new growth percentage
        previous_balance = starting_balance[user]
        new_balance = previous_balance * (1 + new_growth_percentage / 100)
        starting_balance[user] = new_balance
        st.write(f"New balance for {user}: {new_balance}")
    else:
        st.write(f"User {user} not found!")

# Streamlit UI for Admin to set a new growth percentage
st.sidebar.title("Admin Settings")
user_input = st.sidebar.selectbox("Select User", list(starting_balance.keys()))
growth_input = st.sidebar.number_input("Set Growth Percentage", min_value=0, max_value=100, step=1)
if st.sidebar.button("Update Growth"):
    set_new_growth_percentage(user_input, growth_input)

# Display the updated starting balances in Streamlit
st.write("Updated Starting Balances:")
st.write(starting_balance)

# Now, you can define a function to search for a user's wallet and see growth
def view_user_wallet(username):
    if username in starting_balance:
        st.write(f"Wallet for {username}: {starting_balance[username]}")
    else:
        st.write(f"User {username} not found!")

# Streamlit UI for users to view their wallet
user_wallet_input = st.text_input("Enter your username to view wallet")
if user_wallet_input:
    view_user_wallet(user_wallet_input)
