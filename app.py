import json
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Load the credentials from Streamlit secrets
credentials_info = json.loads(st.secrets["credentials_json"])  # Convert the JSON string into a dictionary

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate using the service account credentials
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)

# Proceed with your app logic here
