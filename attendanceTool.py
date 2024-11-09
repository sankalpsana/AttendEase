import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up the service account credentials
SERVICE_ACCOUNT_FILE = '.venv/Keys/micro-weaver-296313-e99ef197034a.json'  # Path to your service account JSON file
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Create credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Sheets API service
service = build('sheets', 'v4', credentials=credentials)

# Define your Spreadsheet ID and range
SPREADSHEET_ID = '1tDj0mfNdV-xWHTBil7TvwCwihgIkHy7g4U7G9V9rgXY'  # Replace with your spreadsheet ID
RANGE_NAME = 'sub1!A:A'  # Adjust the range according to where the student IDs are located

'''
def add_student_to_all_sheets(student_id):
    """Add the student ID to all worksheets present in the spreadsheet."""

    # Step 1: Get all the sheet names in the spreadsheet
    sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', [])

    # Step 2: Loop through all sheets
    for sheet in sheets:
        sheet_name = sheet['properties']['title']  # Get the sheet name
        RANGE_NAME = f'{sheet_name}!A:A'  # Assuming student IDs are in column A

        # Step 3: Read the student ID column to check for existing student IDs
        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        existing_ids = result.get('values', [])

        # Check if student ID already exists
        if any(student_id in row for row in existing_ids):
            print(f"Student ID {student_id} already exists in sheet '{sheet_name}'.")
            continue

        # Step 4: Append the new student ID
        body = {
            'values': [[student_id]]  # Add the student ID as a new row
        }

        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()

        print(f"Added student ID {student_id} to sheet '{sheet_name}'.")


def mark_attendance(student_id, status, date_str, sheet_name):
    """Mark 'Present' or 'Absent' for a specific student on a given date in a specified sheet."""

    # Step 1: Read the entire sheet data
    RANGE_NAME = f'{sheet_name}!A:Z'  # Dynamic range based on the provided sheet name
    sheet = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = sheet.get('values', [])

    if not values:
        print("No data found.")
        return

    # Step 2: Use the provided date as a string
    formatted_date = date_str  # Treat date_str directly as a string

    # Step 3: Find the date column or add a new date column
    header = values[0]  # First row is considered the header row with dates
    if formatted_date not in header:
        # Add a new column with the provided date
        header.append(formatted_date)
        col_index = len(header) - 1  # Get the index of the new column
    else:
        # Find the index of the provided date column
        col_index = header.index(formatted_date)

    # Step 4: Find the student row
    student_row = None
    for row_index, row in enumerate(values):
        if len(row) > 0 and row[0] == student_id:  # Assuming student IDs are in column A
            student_row = row_index
            break

    if student_row is None:
        print(f"Student ID {student_id} not found.")
        return

    # Step 5: Mark 'Present' or 'Absent' in the corresponding date column
    while len(values[student_row]) <= col_index:
        values[student_row].append('')  # Ensure the row has enough columns

    values[student_row][col_index] = status  # Mark the attendance as 'Present' or 'Absent'

    # Step 6: Update the entire sheet with the new values
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()

    print(f"Attendance for student ID {student_id} on {formatted_date} in sheet '{sheet_name}' marked as '{status}'.")
'''
def add_student_to_all_sheets(student_id):
    """Add the student ID to all worksheets present in the spreadsheet."""

    # Step 1: Get all the sheet names in the spreadsheet
    sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', [])

    # Step 2: Loop through all sheets
    for sheet in sheets:
        sheet_name = sheet['properties']['title']  # Get the sheet name
        RANGE_NAME = f'{sheet_name}!A:A'  # Assuming student IDs are in column A

        # Step 3: Read the student ID column to check for existing student IDs
        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        existing_ids = result.get('values', [])

        # Check if student ID already exists
        if any(student_id in row for row in existing_ids):
            print(f"Student ID {student_id} already exists in sheet '{sheet_name}'.")
            continue

        # Step 4: Append the new student ID
        body = {
            'values': [[student_id]]  # Add the student ID as a new row
        }

        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()

        print(f"Added student ID {student_id} to sheet '{sheet_name}'.")


def mark_attendance(detected_students, status, date_str, sheet_name):
    """Mark 'Present' or 'Absent' for a specific student on a given date in a specified sheet."""

    # Step 1: Read the entire sheet data
    RANGE_NAME = f'{sheet_name}!A:Z'  # Dynamic range based on the provided sheet name
    sheet = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = sheet.get('values', [])

    if not values:
        print("No data found.")
        return

    # Step 2: Use the provided date as a string
    formatted_date = date_str  # Treat date_str directly as a string

    # Step 3: Find the date column or add a new date column
    header = values[0]  # First row is considered the header row with dates
    if formatted_date not in header:
        # Add a new column with the provided date
        header.append(formatted_date)
        col_index = len(header) - 1  # Get the index of the new column
    else:
        # Find the index of the provided date column
        col_index = header.index(formatted_date)

    # Step 4: Find the student row
    for student_id in detected_students:
        student_row = None
        for row_index, row in enumerate(values):
            if len(row) > 0 and row[0] == student_id:  # Assuming student IDs are in column A
                student_row = row_index
                break

        if student_row is None:
            print(f"Student ID {student_id} not found.")
            return

        # Step 5: Mark 'Present' or 'Absent' in the corresponding date column
        while len(values[student_row]) <= col_index:
            values[student_row].append('')  # Ensure the row has enough columns

        values[student_row][col_index] = status  # Mark the attendance as 'Present' or 'Absent'

        # Step 6: Update the entire sheet with the new values
        body = {
            'values': values
        }
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()
    print("Attendance updated successfully for all detected students.")

# Example usage
#add_student_id_to_all_sheets('21eg105e00022')  # Replace 'S1001' with the student ID you want to add
#mark_attendance('21eg105e00022', 'Present', '2024-10-15', 'sub1')


