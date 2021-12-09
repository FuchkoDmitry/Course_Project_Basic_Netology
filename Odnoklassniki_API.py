import requests
import hashlib


class OkApi:
    def __init__(self, token, ssk, app_key):
        self.url = 'https://api.ok.ru/api/'
        self.SSK = ssk
        self.token = token
        self.AppKey = app_key

    def get_user_photos(self, user_id, count=20):
        '''
        загрузить фотографии пользователя по user_id.
        для получения своих фото необходимо ввести свой user_id
        '''
        user_photos = dict()
        photos_url = self.url + 'photos/getUserPhotos'
        photos_params = {'application_key': self.AppKey,
                         'fid': user_id,
                         'access_token': self.token,
                         'method': 'photos.getUserPhotos',
                         'count': count
                         }
        while True:
            photos_params['sig'] = self.add_mb5_sig(photos_params)
            response = requests.get(photos_url, params=photos_params).json()
            del photos_params['sig']
            if response['hasMore'] or response['photos']:
                for photo in response['photos']:
                    photos_params['pagingAnchor'] = response['pagingAnchor']
                    if photo['mark_count'] not in user_photos:
                        user_photos[photo['mark_count']] = [photo['standard_url'], photo['mod_status']]
                    else:
                        user_photos[f"{photo['mark_count']}_{photo['fid']}"] = [photo['standard_url'],
                                                                                photo['mod_status']]
            else:
                return user_photos

    def get_user_albums(self, user_id, count=20):
        #  для получения своих альбомов необходимо ввести свой user_id
        user_albums = []
        user_albums_url = self.url + 'photos/getAlbums'
        user_albums_params = {'application_key': self.AppKey,
                              'fid': user_id,
                              'access_token': self.token,
                              'method': 'photos.getAlbums',
                              'count': count
                              }
        while True:
            user_albums_params['sig'] = self.add_mb5_sig(user_albums_params)
            response = requests.get(user_albums_url, params=user_albums_params).json()
            del user_albums_params['sig']
            if 'hasMore' in response.keys():
                for album in response['albums']:
                    user_albums.append(album['aid'])
                    user_albums_params['pagingAnchor'] = response['pagingAnchor']
            else:
                return user_albums

    def get_albums_photos(self, albums_list, count=100):
        # параметр count - количество получаемых фотографий каждого альбома(максимум 100)
        albums_photos = {}
        albums_photos_url = self.url + 'photos/getUserAlbumPhotos'
        albums_photos_params = {'application_key': self.AppKey,
                                'access_token': self.token,
                                'method': 'photos.getUserAlbumPhotos',
                                'count': count
                                }
        for album in albums_list:
            albums_photos_params['aid'] = album
            albums_photos_params['sig'] = self.add_mb5_sig(albums_photos_params)
            response = requests.get(albums_photos_url, params=albums_photos_params).json()
            del albums_photos_params['sig']
            for photo in response['photos']:
                if photo['mark_count'] not in albums_photos:
                    albums_photos[photo['mark_count']] = [photo['standard_url'], photo['mod_status']]
                else:
                    albums_photos[f"{photo['mark_count']}_{photo['fid']}"] = [photo['standard_url'], photo['mod_status']]
        return albums_photos

    def add_mb5_sig(self, params):
        signature_data = params.copy()
        [signature_data.pop(key, '') for key in ['session_key', 'access_token']]
        lexicograph = sorted(signature_data.items())
        string_payload = ''
        for pair in lexicograph:
            string_payload = f'{string_payload}{pair[0]}={pair[1]}'
        sig = hashlib.md5(f'{string_payload}{self.SSK}'.encode()).hexdigest()
        signature_data['sig'] = sig
        return sig











