import requests
import time
from tqdm import tqdm


class InstUser:
    def __init__(self, token, user_id):
        self.url = f'https://graph.instagram.com/v12.0/{user_id}/'
        self.params = {'access_token': token}

    def get_max_media_list(self, count):
        '''
        Решил реализовать через функцию range, так как количество
        запросов к API ограничено 200 в час. Можно конечно в этом
        методе загрузить все медиафайлы, а в методе get_user_photos
        поставить time.sleep, но это будет очень медленно.
        '''
        photos_list = []
        all_media_url = self.url + 'media'
        all_media_params = {'limit': count}
        for i in range(2):
            try:
                response = requests.get(all_media_url,
                                        params={**self.params,
                                                **all_media_params
                                                }
                                        )
                response.raise_for_status()
            except requests.exceptions.RequestException as error:
                raise SystemExit(error)

            for photo in response.json()['data']:
                photos_list.append(photo['id'])
            if 'next' in response.json()['paging']:
                all_media_params['after']\
                    = response.json()['paging']['cursors']['after']
            else:
                return photos_list
        return photos_list

    def get_media_list(self, count=5):
        # максимальное значение парметра count=100
        photos_list = []
        media_url = self.url + 'media'
        media_params = {'limit': count}
        try:
            response = requests.get(media_url,
                                    params={**self.params, **media_params}
                                    )
            time.sleep(0.33)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        for photo in response.json()['data']:
            photos_list.append(photo['id'])
        return photos_list

    def get_user_photos(self, photos_list):
        user_photos = dict()
        user_photos_params = {'fields': 'id,media_url,media_type'}
        for photo in tqdm(photos_list):
            url = f'https://graph.instagram.com/{photo}'
            try:
                response = requests.get(url,
                                        params={**self.params,
                                                **user_photos_params
                                                }
                                        )
                response.raise_for_status()
                user_photos[response.json()['id']] \
                    = [response.json()['media_url'],
                       response.json()['media_type']
                       ]
            except requests.exceptions.RequestException as error:
                raise SystemExit(error)
        print('photos downloaded')
        return user_photos
