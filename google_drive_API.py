'''
Создаем сервисный аккаунт. Получаем ключ аккаунта в json формате,
сохраняем его в рабочей директории. Устанавливаем клиентскую библиотеку
Google API(pip install --upgrade google-api-python-client).
Импортируем необходимые модули(ниже).
Создаём папку на google диске, открываем в ней доступ для сервисного аккаунта.
'''

from google.oauth2 import service_account
from googleapiclient.http import MediaInMemoryUpload
from googleapiclient.discovery import build
import requests
import time
from tqdm import tqdm
from YaUploader import get_photos_info_json


class GoogleDriveUploader:
    #  указываем необходимые доступы SCOPES.
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # указываем путь к файлу с ключами сервисного аккаунта.
    SERVICE_ACCOUNT_FILE = ''

    # указываем id созданной ранее папки.
    # Узнать, открыв с браузере и скопировав из url
    folder_id = ''

    # создаем учетные данные указав путь к файлу с ключами доступа и scopes
    credentials = service_account.Credentials.\
        from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # создаем сервис, который будет использовать REST API
    # Google Drive отправляя запросы из учетных данных
    service = build('drive', 'v3', credentials=credentials)

    def create_folder(self, folder_name):
        file_metadata = {'name': folder_name,
                         'mimeType': 'application/vnd.google-apps.folder',
                         'parents': [self.folder_id]
                         }
        response = self.service.files().create(body=file_metadata,
                                               fields='id').execute()
        return response['id']

    def upload_photos(self, folder_name, photos_list):
        downloads_photos_info = []
        created_folder = self.create_folder(folder_name)
        for photo_name, photo_url in tqdm(photos_list.items()):
            downloads_photos_info.append({'file_name': f'{photo_name}.jpg',
                                          'size': photo_url[1]}
                                         )
            time.sleep(0.2)
            name = f'{photo_name}.jpg'
            file = requests.post(photo_url[0]).content
            file_metadata = {'name': name, 'parents': [created_folder]}
            media = MediaInMemoryUpload(file, resumable=True)
            try:
                self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
            except requests.exceptions.RequestException as error:
                raise SystemExit(error)
        print('Photos uploaded')
        return get_photos_info_json(downloads_photos_info)

    def upload_ig_photos(self, folder_name, photos_list):
        downloads_photos_info = []
        created_folder = self.create_folder(folder_name)
        for photo_name, photo_url in tqdm(photos_list.items()):
            downloads_photos_info.append({'file_name': f'{photo_name}.jpg',
                                          'size': photo_url[1]}
                                         )
            time.sleep(0.2)
            name = f'{photo_name}.jpg'
            file = requests.get(photo_url[0]).content
            file_metadata = {'name': name, 'parents': [created_folder]}
            media = MediaInMemoryUpload(file, resumable=True)
            try:
                self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
            except requests.exceptions.RequestException as error:
                raise SystemExit(error)
        print('Photos uploaded')
        return get_photos_info_json(downloads_photos_info)
