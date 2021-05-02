from flask import Flask, render_template

import os

from googleapiclient.discovery import build
from google.oauth2 import service_account

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/data')
def load_data():
    service = build('sheets', 'v4', credentials=ACCOUNT_INFO)
    spreadsheet_id = os.environ.get("GOOGLE_SPREADSHEET_ID")
    range_name = os.environ.get("GOOGLE_CELL_RANGE")

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    d = {}
    data = []
    i = 0

    for value in values:
        while len(value) < 12:
            value.append("")
        
        temp = {}
        temp["timestamp"] = value[0]
        temp["name"] = value[1]
        temp["email"] = value[2]
        temp["phone"] = value[3]
        temp["disabilities"] = value[4]
        temp["waiver"] = value[5]
        temp["assistance"] = value[6]
        temp["address"] = value[7]
        temp["program"] = value[8]
        if value[9] == "":
            temp["boat"] = value[10]
        else:
            temp["boat"] = value[9]
        temp["additional"] = value[11]
        data.append(temp)

    data.pop(0)
    d["data"] = data
    return d

def get_account_info():
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    GOOGLE_PRIVATE_KEY = os.environ["GOOGLE_PRIVATE_KEY"]
    # The environment variable has escaped newlines, so remove the extra backslash
    GOOGLE_PRIVATE_KEY = GOOGLE_PRIVATE_KEY.replace('\\n', '\n')

    account_info = {
        "private_key": GOOGLE_PRIVATE_KEY,
        "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
        "token_uri": "https://accounts.google.com/o/oauth2/token",
    }

    credentials = service_account.Credentials.from_service_account_info(
        account_info, scopes=scopes)
    return credentials


# Get Creds: https://developers.google.com/sheets/api/quickstart/python?authuser=4
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
ACCOUNT_INFO = get_account_info()