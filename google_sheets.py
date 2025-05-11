import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import tempfile

class GoogleSheetsClient:
    def __init__(self, spreadsheet_id, credentials_json_env):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

        # Parse JSON from environment variable and write to a temporary file
        credentials_dict = json.loads(credentials_json_env)
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_json:
            json.dump(credentials_dict, temp_json)
            temp_json_path = temp_json.name

        creds = ServiceAccountCredentials.from_json_keyfile_name(temp_json_path, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(spreadsheet_id)
        self.attendance_sheet = self.sheet.worksheet('Obecności')
        self.summary_sheet = self.sheet.worksheet('Podsumowanie')

    def record_attendance(self, date, members, leader):
        for member in members:
            self.attendance_sheet.append_row([date, member, leader])

    def get_monthly_summary(self):
        records = self.attendance_sheet.get_all_records()
        points = {}
        leaders = {}
        for rec in records:
            date = datetime.strptime(rec['Data'], "%Y-%m-%d")
            if date.month == datetime.now().month:
                points[rec['Użytkownik']] = points.get(rec['Użytkownik'], 0) + 1
                leaders[rec['Raid Leader']] = leaders.get(rec['Raid Leader'], 0) + 1
        return {'points': points, 'leaders': leaders}
