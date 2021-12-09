import json
import requests
import time
from tqdm import tqdm


class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'
                }

    def create_folder(self, dir_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {'path': dir_name}
        requests.put(url, headers=headers, params=params)

    def upload_photos_to_disk(self, path_to_file, files_to_upload):
        downloads_photos_info = []
        self.create_folder(path_to_file)
        headers = self.get_headers()
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        for photo_name, photo_url in tqdm(files_to_upload.items()):
            downloads_photos_info.append({'file_name': f'{photo_name}.jpg',
                                          'size': photo_url[1]}
                                         )
            time.sleep(0.3)
            params = {'path': f'{path_to_file}/{photo_name}',
                      'url': photo_url[0]}
            requests.post(url=url, params=params, headers=headers)
        print('photos uploaded')
        return get_photos_info_json(downloads_photos_info)


def get_photos_info_json(photos_file):
    with open('uploads_photos_info.json', 'w', encoding='utf-8') as file:
        json.dump(photos_file, file, indent=2, ensure_ascii=False)
