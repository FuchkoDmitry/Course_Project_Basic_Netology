import requests
import time


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {'access_token': token, 'v': version}

    def get_photos(self, user_id=None, count=50, album_id='profile'):
        '''
        получить фото со стены album_id='wall'
        получить сохраненные фото album_id='saved'
        по-умолчанию аватарки пользователя
        '''
        profile_photos = dict()
        profile_photo_url = self.url + 'photos.get'
        profile_photo_params = {'owner_id': user_id, 'album_id': album_id,
                                'extended': 1, 'photo_sizes': 1, 'count': count
                                }
        response = requests.get(profile_photo_url,
                                params={**self.params, **profile_photo_params}).json()['response']['items']
        for photo in response:
            if photo['likes']['count'] not in profile_photos:
                profile_photos[photo['likes']['count']] = [photo['sizes'][-1]['url'], photo['sizes'][-1]['type']]
            else:
                profile_photos[f"{photo['likes']['count']}_{photo['date']}"] = \
                    [photo['sizes'][-1]['url'], photo['sizes'][-1]['type']]
        return profile_photos

    def get_albums_photos(self, user_id=None, count=200):
        # получаем фото из всех альбомов пользователя
        albums_photos = dict()
        albums_photos_url = self.url + 'photos.getAll'
        albums_photos_params = {'owner_id': user_id, 'extended': 1, 'photo_sizes': 1,
                                'count': count, 'no_service_albums': 1, 'offset': 0, 'skip_hidden': 1
                                }
        while True:
            response = requests.get(albums_photos_url,
                                    params={**self.params, **albums_photos_params}).json()['response']
            time.sleep(0.33)
            if 'more' in response.keys():
                for photo in response['items']:
                    if photo['likes']['count'] not in albums_photos:
                        albums_photos[photo['likes']['count']] = [photo['sizes'][-1]['url'],
                                                                  photo['sizes'][-1]['type']
                                                                  ]
                    else:
                        albums_photos[f"{photo['likes']['count']}_{photo['date']}"] = [photo['sizes'][-1]['url'],
                                                                                       photo['sizes'][-1]['type']
                                                                                       ]
                albums_photos_params['offset'] += count
            else:
                return albums_photos




