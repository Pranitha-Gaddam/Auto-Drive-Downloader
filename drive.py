import os
import os.path
# import schedule
#import time
# import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#from Google import Create_Service
#from googleapiclient.http import MediaIoBaseDownload

CLIENT_SECRET_FILE = r'C:\Users\Pranitha\OneDrive - UNT System\Desktop\driveDownloader\credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
#TOKEN_FILE = 'token.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

LOCAL_FOLDER = r'C:\Users\Pranitha\OneDrive - UNT System\Desktop\local folder'

#service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
"""
def authDrive():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)

    #if TOKEN_FILE != None:
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())
    
    return creds
"""
def listFiles(service, folderID):
    results = service.files().list(q=f"'{folderID}' in parents", fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])
    return files

def downloadFiles(service, file_id, LOCAL_FOLDER):
    #results = service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name, mimeType)").execute()
    #videos = results.get('files', [])
    request = service.files().get_media(fileId = file_id)
    fileInfo = service.files().get(fileId = file_id, fields = "name").execute()
    fileName = fileInfo.get('name', '')
    filePath = os.path.join(LOCAL_FOLDER, fileName)
    #if not videos:
    #   print('No videos found.')
    """
        for video in videos:
            videoID = video['id']
            videoName = video['name']
            print(f'Downloading video: {videoName} (ID: {videoID})')

            # downloading the video content
            request = service.files().get_media(fileId=videoID)
            filePath = os.path.join(LOCAL_FOLDER, videoName)"""

    with open(filePath, 'wb') as file:
        file.write(request.execute())

    print(f'File downloaded: {fileName}')

def main():
    """
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        creds = authDrive()"""
    """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
    creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            r"C:\Users\Pranitha\OneDrive - UNT System\Desktop\driveDownloader\credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        print('port command ran\n')
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

    service = build(API_NAME, API_VERSION, credentials=creds)

    driveFolderID = '1m9eQccOl0iWdYD5E4iBgUToJS4ZWBO2b'

    driveFiles = listFiles(service, driveFolderID)
    #localFiles = [file for file in os.listdir(LOCAL_FOLDER) if os.path.isfile(os.path.join(LOCAL_FOLDER, file))]
    localFiles = set([file.replace(".id", "") for file in os.listdir(LOCAL_FOLDER) if os.path.isfile(os.path.join(LOCAL_FOLDER, file))])
    filesToDownload = [file for file in driveFiles if file['id'] not in localFiles]

    for file in filesToDownload:
        downloadFiles(service, file['id'], LOCAL_FOLDER)
"""
schedule.every(2).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
"""
if __name__ == "__main__":
  main()