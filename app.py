import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["credentials_json"], scope)

# Authorize the client
gc = gspread.authorize(credentials)

# List all spreadsheets available to the service account
spreadsheet_list = gc.openall()
for sheet in spreadsheet_list:
    print(sheet.title)
