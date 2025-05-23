import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np

# Configuration
SHEET_NAME = "divine_fund_bank"  # Google Sheet name
CREDENTIALS_JSON = st.secrets["credentials_json"]  # Streamlit secrets for the credentials

# Google Sheets API setup
def authenticate_google_sheets():
    """Authenticate using service account credentials."""
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(CREDENTIALS_JSON, scope)
        gc = gspread.authorize(credentials)
        return gc
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return None

# Load data from Google Sheets
def load_sheet_data(gc):
    """Load sheet data into a pandas DataFrame."""
    try:
        # Open the Google Sheet by name
        sh = gc.open(SHEET_NAME)
        # Assuming the first sheet is the relevant one
        worksheet = sh.get_worksheet(0)
        # Fetch all records
        data = worksheet.get_all_records()
        if not data:
            st.warning("No data found in the sheet!")
        else:
            return pd.DataFrame(data)
    except gspread.SpreadsheetNotFound:
        st.error(f"Spreadsheet '{SHEET_NAME}' not found.")
        return None
    except Exception as e:
        st.error(f"Error loading sheet data: {e}")
        return None

# Display the data in the Streamlit app
def display_data(df):
    """Display the dataframe in Streamlit."""
    if df is not None:
        st.write("### Data from the Google Sheet")
        st.dataframe(df)
    else:
        st.write("No data to display.")

# Add deposit logic
def handle_deposit():
    """Handle user deposit for pooling."""
    st.write("### Make a Deposit")
    deposit_quantity = st.number_input("Enter the quantity you want to deposit", min_value=1, step=1)
    if st.button("Deposit"):
        if deposit_quantity > 0:
            st.success(f"You have successfully deposited {deposit_quantity} items.")
        else:
            st.error("Please enter a valid quantity.")

# Add pooling logic
def handle_pooling():
    """Handle pooling logic for profit distribution."""
    st.write("### Pooling Information")
    share_percentage = st.slider("Select your share percentage in the pool", 1, 100, 10)
    total_profit = st.number_input("Enter the total profit from pooled items", min_value=0.0)
    if st.button("Distribute Profit"):
        if total_profit > 0:
            profit_share = (share_percentage / 100) * total_profit
            st.success(f"Your share of the total profit is: {profit_share:.2f} currency.")
        else:
            st.error("Please enter a valid total profit.")

# Main app function
def main():
    st.title("Divine Fund Bank")
    
    gc = authenticate_google_sheets()
    if gc:
        # Load data
        df = load_sheet_data(gc)
        display_data(df)
        
        # Handling user actions (Deposit and Pooling)
        handle_deposit()
        handle_pooling()
    else:
        st.error("Unable to authenticate Google Sheets API.")

# Run the app
if __name__ == "__main__":
    main()
