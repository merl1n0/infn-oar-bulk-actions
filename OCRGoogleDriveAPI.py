from __future__ import print_function
import httplib2
import os
import io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument("path", help="folder path of the PDF files to OCR")
    flags = parser.parse_args()
except ImportError:
    flags = None


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # credential_path = os.path.join("./", 'drive-python-quickstart.json')
    credential_path = "token.json"
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # per eseguire OCR dei pdf in sequenza
    # esempio: da 1 a 24 (inclusi)  ---> range(1, 25)
    x = range(2, 3)

    file_list = os.listdir(flags.path)
    for file in file_list:
        # Image with texts (png, jpg, bmp, gif, pdf)
        if not file.endswith(".pdf"):
            continue
        imgfile = os.path.join(flags.path, file)
        # Text file outputted by OCR
        txtfile = os.path.join(flags.path, "output",
                               file.replace("pdf", "txt"))

        mime = 'application/vnd.google-apps.document'
        print(f"Uploading {imgfile} to Google Drive")
        res = service.files().create(
            body={
                'name': imgfile,
                'mimeType': mime
            },
            media_body=MediaFileUpload(imgfile, mimetype=mime, resumable=True)
        ).execute()

        print(f"Converting and saving to {txtfile}")

        if not os.path.isdir(os.path.join(flags.path, "output")):
            os.mkdir(os.path.join(flags.path, "output"))

        downloader = MediaIoBaseDownload(
            io.FileIO(txtfile, 'wb'),
            service.files().export_media(
                fileId=res['id'], mimeType="text/plain")
        )
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        service.files().delete(fileId=res['id']).execute()
        print("Done.\n")


if __name__ == '__main__':
    main()
