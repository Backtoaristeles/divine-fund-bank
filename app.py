import streamlit as st
import json
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Setup Google Sheets API credentials from Streamlit secrets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
credentials_info = json.loads(st.secrets["credentials_json"])
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
gc = gspread.authorize(credentials)

# Open your sheet by name
SHEET_NAME = "divine_fund_bank"  # Replace with the exact name of your sheet
sh = gc.open(SHEET_NAME)

# Load deposits data
worksheet = sh.worksheet("deposits")  # Tab must be called 'deposits'
data = worksheet.get_all_records()
df = pd.DataFrame(data)

st.title("Divine Fund Bank")

# Show total current fund value
total_fund = df['amount'].astype(float).sum()
st.metric("💰 Total Fund Value (Divines)", f"{total_fund:.2f}")

# Simple user wallet search
user_search = st.text_input("🔎 Search for your wallet (enter username):")
if user_search:
    user_df = df[df['user'].str.lower() == user_search.lower()]
    st.subheader(f"Wallet for {user_search}")
    st.write(user_df)
    st.write(f"**Total deposited:** {user_df['amount'].astype(float).sum():.2f} Divines")

# Show all deposits
st.subheader("All Deposits")
st.dataframe(df)

st.info("This is the basic version. Add more features as needed!")
