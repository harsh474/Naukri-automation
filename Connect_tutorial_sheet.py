import gspread
from google.oauth2.service_account import Credentials

# Define the scope
scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# Authenticate using service account
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Open the Google Sheet by ID
sheet_id = "1VGVjRB_1LmSAxyc6k5Z0M-_tRdD2VNkF5yacO4wD2jk"
workbook = client.open_by_key(sheet_id)

# Data to insert
values = [
    ["Basketball", 29.99, 1],
    ["Jeans", 39.99, 4],
    ["Soap", 7.99, 3],
]

def add_row_in_sheet(values):
     # Target worksheet
     new_worksheet_name = "Sheet1"
     sheet = workbook.worksheet(new_worksheet_name)

     # Find the last non-empty row
     last_row = len(sheet.get_all_values())

     # If it's a fresh sheet (only headers), optionally write header
     if last_row == 0:
     sheet.update(range_name="A1:C1", values=[["Name", "Price", "Quantity"]])
     last_row = 1  # Next data starts at row 2

     # Now write new values starting from the next row
     range_to_update = f"A{last_row + 1}:C{last_row + len(values)}"
     sheet.update(range_name=range_to_update, values=values)

     print(f"Appended {len(values)} rows to '{new_worksheet_name}' starting at row {last_row + 1}")
