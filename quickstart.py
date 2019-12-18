from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
from config import Config, config


def get_spreadsheet(SCOPES, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')

    df = pd.DataFrame(values[1:], columns=values[0])
    for col in df.columns:
        df[col] = df[col].str.encode('ascii', 'ignore').str.decode('utf-8').str.replace(',', '.')
    return df


if __name__ == '__main__':
    li_df = []
    for srn in Config.SAMPLE_RANGE_NAMES:
        li_df.append(get_spreadsheet(Config.SCOPES, Config.SAMPLE_SPREADSHEET_ID, srn))

    df = pd.concat(li_df, axis=0, sort=False).reset_index(drop=True)
    # TODO fixer pour enlever ce filtre
    df = df[df.date_devis != '']
    df.date_devis = pd.to_datetime(df.date_devis, format='%d/%m/%Y')
