import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd

# Google Sheets API connection
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["credentials_json"], scope)
gc = gspread.authorize(credentials)

# Define the sheet name
SHEET_NAME = "divine_fund_bank"

try:
    # Open the Google Sheet by name
    sh = gc.open(SHEET_NAME)
    worksheet = sh.get_worksheet(0)  # You can specify which sheet by index or by name
    data = worksheet.get_all_records()  # Fetch all rows as a list of dictionaries

    # Convert to DataFrame for easier handling in Streamlit
    df = pd.DataFrame(data)

    # Display the DataFrame in Streamlit
    st.write("Data from Google Sheets:")
    st.dataframe(df)  # Display the data

except gspread.SpreadsheetNotFound:
    st.error(f"The sheet named '{SHEET_NAME}' could not be found.")
except Exception as e:
    st.error(f"An error occurred: {e}")
