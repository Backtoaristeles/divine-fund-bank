import json
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import gspread

# Fetch credentials from Streamlit secrets
credentials_info = st.secrets["credentials_json"]

# Ensure the credentials_info is in dictionary format, if it's a string
if isinstance(credentials_info, str):
    credentials_info = json.loads(credentials_info)

# Define the scope for Google Sheets and Google Drive
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate using the service account credentials
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)

# Authorize the credentials with gspread
gc = gspread.authorize(credentials)

# Open the Google Sheet by its name
SHEET_NAME = "divine_fund_bank"  # Use the correct sheet name here

try:
    sh = gc.open(SHEET_NAME)
    print(f"Successfully opened the sheet: {SHEET_NAME}")
except gspread.SpreadsheetNotFound:
    print(f"Error: The sheet named '{SHEET_NAME}' could not be found.")
