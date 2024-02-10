import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
from registration import registration_form
# functiont to fetch data from google sheets


def fetch_google_sheets_data():
    # Define the scope for accessing Google Sheets
    scope = ["https://spreadsheets.google.com/feeds"]
    keyfile_path = "/Users/taliarosenkranz/Documents/Projects/Volunteering/volunteeringisrael-3504ebfd1ca0.json"
    # Load credentials from credentials JSON file
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        keyfile_path, scope)

    # Authorise access to Google Sheets
    client = gspread.authorize(creds)

    # Open Google Sheets document by its ID
    sheet = client.open_by_key("1aCFF6Bivvj9NlqODHWn2ifWO0J-iwVTNMsu7U68nRjg")
    # Select worksheet by its title
    worksheet = sheet.worksheet("Locations")

    # Get all values from worksheet
    data = worksheet.get_all_values()

    return data


# Fetch data from Google Sheets
sheet_data = fetch_google_sheets_data()

print(sheet_data)


def upload_registration_data(organization_data):

    # Define the scope for accessing Google Sheets
    scope = ["https://spreadsheets.google.com/feeds"]
    keyfile_path = "/Users/taliarosenkranz/Documents/Projects/Volunteering/volunteeringisrael-3504ebfd1ca0.json"
    # Load credentials from credentials JSON file
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        keyfile_path, scope)

    # Authorise access to Google Sheets
    client = gspread.authorize(creds)

    # Open Google Sheets document by its ID
    sheet = client.open_by_key("1aCFF6Bivvj9NlqODHWn2ifWO0J-iwVTNMsu7U68nRjg")
    # Select worksheet by its title
    worksheet = sheet.worksheet("RegistrationDetails")
    # Write the data to the Google Sheets document
    worksheet.append_row(organization_data)
