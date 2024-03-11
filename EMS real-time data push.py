import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import serial
import os
import re

# Print the current working directory
print("Current Working Directory:", os.getcwd())

# Arduino Serial Port
ser = serial.Serial('COM5', 9600)  # Change 'COM3' to your Arduino port

# Google Sheets Credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials_path = r'C:\Users\Admin\Downloads\my-energy-meter-723058b6dbbf.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)

gc = gspread.authorize(credentials)
spreadsheet_key = '1p1PXK1unzp2pbiYwMM5XnwhmeLr2YXapAaWEYTYUmOk'  # Replace with your actual spreadsheet key

worksheet = gc.open_by_key(spreadsheet_key).sheet1

# Add column names programmatically
column_names = ['Time (s)', 'Current (A)', 'Voltage (V)', 'Power (W)']
worksheet.insert_row(column_names, index=1)

while True:
    # Get current time in seconds
    current_time = int(time.time())

    # Read data from Arduino
    arduino_data = ser.readline().decode('utf-8').strip()

    # Print the raw data for debugging
    print("Raw Arduino Data:", arduino_data)

    # Use regular expressions to extract numerical values
    match = re.match(r"Voltage \(V\): ([0-9.]+)\t Current \(A\): ([0-9.]+)\t Power \(W\): ([0-9.]+)", arduino_data)
    
    if match:
        try:
            # Extract numerical values
            voltage, current, power = [float(match.group(i + 1)) for i in range(3)]

            # Send data to Google Sheets
            worksheet.append_row([current_time, current, voltage, power])

            print(f"Time (s): {current_time}\tVoltage (V): {voltage}\tCurrent (A): {current}\tPower (W): {power}")

        except ValueError as e:
            print(f"Error converting data: {e}")
            continue

    time.sleep(1)
