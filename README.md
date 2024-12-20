Face Recognition Attendance System
This project is a real-time face recognition attendance tracking system using Flask, Google Sheets, and OpenCV. It includes two main functionalities:

Marking Attendance: Recognizes faces in live video stream and records attendance in Google Sheets for a selected date and subject.
Adding Students: Adds new student IDs to all subjects' sheets if not already present.
Table of Contents
Features
Technologies
Project Setup
Usage
File Structure
Future Improvements
Features
Real-time Face Recognition: Uses a live video feed to detect and recognize faces.
Attendance Tracking: Updates Google Sheets to mark attendance for each recognized student, including date and subject.
Student Management: Adds new student IDs across all subject sheets to maintain a consistent record.
JavaScript and Flask Integration: Streamlines user interaction with forms and real-time video feed updates.
Technologies
Python (Flask, OpenCV)
JavaScript for handling form inputs and video stream
Google Sheets API to store and retrieve attendance records
HTML/CSS for the frontend interface
Project Setup
Clone the Repository

git clone https://github.com/your-username/face-recognition-attendance-system.git
cd face-recognition-attendance-system
Install Dependencies Create a virtual environment and install required packages:

python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
pip install -r requirements.txt
Google Sheets API Setup

Set up a Google Cloud Project and enable the Google Sheets API.
Download the credentials JSON file and save it in .venv/Keys/.
Update the SERVICE_ACCOUNT_FILE in your code to match this path.
Configuration Update SPREADSHEET_ID with your Google Sheets ID and adjust the sheet names in RANGE_NAME as necessary.

Usage
Running the Application
Start the Flask server

flask run
Access the Web Interface Go to http://127.0.0.1:5000 in your browser.

Functions

Add Student: Click "Add Student" to add a new student ID to all sheets.
Take Attendance: Enter date and subject, then click "Start Stream" to start the live video feed and automatically log attendance for detected students.
Code Walkthrough
main.py: Main Flask app with routes for capturing attendance and adding students.
attendanceTool.py: Contains functions to interact with Google Sheets, including marking attendance and adding new students.
templates/index.html: Frontend HTML form with fields for date and subject, buttons to trigger attendance capture, and live video display.
static/js/script.js: JavaScript to handle video stream display and form validation.


Future Improvements
Enhance Error Handling: Improve user feedback for errors like API timeouts.
Add Facial Recognition Model Training: Allow users to add face encodings directly via the web interface.
Data Security: Implement authentication for accessing and updating Google Sheets.
Mobile Compatibility: Make the UI responsive for mobile devices.
Contributing
If you'd like to contribute, please create a fork of this repository, make your changes, and submit a pull request. All contributions are welcome!
