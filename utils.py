from vk_api import VkUser
from Odnoklassniki_API import OkApi
from YaUploader import YaUploader
from instgrm_API import InstUser
from google_drive_API import GoogleDriveUploader

VK_TOKEN = ''
YA_TOKEN = ''
OK_TOKEN = ''
OK_APP_KEY = ''
OK_SSK = ''
insta_token = ''
insta_user_id = ''


def user_interface():
    uploader = YaUploader(YA_TOKEN)
    vk_client = VkUser(VK_TOKEN, '5.131')
    ok_loader = OkApi(OK_TOKEN, OK_SSK, OK_APP_KEY)
    insta_loader = InstUser(insta_token, insta_user_id)
    gd_uploader = GoogleDriveUploader()
    while True:
        print('Выберите соцсеть: 1 - VK, 2 - Odnoklassniki, '
              '3 - Instagram, "exit" - выход')
        social_network = input()
        print('Загружаем фото на: 1 - Яндекс.Диск, '
              '2 - GoogleDrive, "exit" - выход')
        storage = input()
        if social_network == '1' and (storage == '1' or storage == '2'):
            u_id = int(input('Введите id пользователя:'))
            folder = input('введите название папки:')
            print('''
            откуда скачиваем фото?
            1 - стена;
            2 - сохраненные фото;
            3 - аватарки;
            4 - все фото
            ''')
            option = int(input())
            if option == 1:
                photos = vk_client.get_photos(user_id=u_id, album_id='wall')
                if storage == '1':
                    uploader.upload_photos_to_disk(folder, photos)
                else:
                    gd_uploader.upload_photos(folder, photos)
            elif option == 2:
                photos = vk_client.get_photos(user_id=u_id, album_id='saved')
                if storage == '1':
                    uploader.upload_photos_to_disk(folder, photos)
                else:
                    gd_uploader.upload_photos(folder, photos)
            elif option == 3:
                photos = vk_client.get_photos(user_id=u_id)
                if storage == '1':
                    uploader.upload_photos_to_disk(folder, photos)
                else:
                    gd_uploader.upload_photos(folder, photos)
            elif option == 4:
                photos = vk_client.get_albums_photos(user_id=u_id)
                if storage == '1':
                    uploader.upload_photos_to_disk(folder, photos)
                else:
                    gd_uploader.upload_photos(folder, photos)
            else:
                print('неправильный ввод')

        elif social_network == '2' and (storage == '1' or storage == '2'):
            u_id = input('Введите id пользователя:')
            folder = input('введите название папки:')
            print('''
            откуда скачиваем фото?
            1 - аватарки;
            2 - фото из альбомов;
            ''')
            option = int(input())
            if option == 1:
                photos = ok_loader.get_user_photos(u_id)
                if storage == '1':
                    uploader.upload_photos_to_disk(folder, photos)
                else:
                    gd_uploader.upload_photos(folder, photos)
            elif option == 2:
                albums_list = ok_loader.get_user_albums(u_id)
                photos = ok_loader.get_albums_photos(albums_list)
                if storage == '1':
                    uploader.upload_photos_to_disk(folder, photos)
                else:
                    gd_uploader.upload_photos(folder, photos)
            else:
                print('неправильный ввод')

        elif social_network == '3' and (storage == '1' or storage == '2'):
            folder = input('введите название папки:')
            count = int(input('Сколько фото скачиваем?(max=200)'))
            if 1 <= count <= 100:
                photos_list = insta_loader.get_media_list(count=count)
                photos = insta_loader.get_user_photos(photos_list)
                if storage == '1':
                    uploader.upload_photos_to_disk(folder, photos)
                else:
                    gd_uploader.upload_ig_photos(folder, photos)
            elif 100 < count <= 200:
                photos_list = insta_loader.get_max_media_list(count=count/2)
                photos = insta_loader.get_user_photos(photos_list)
                if storage == '1':
                    uploader.upload_photos_to_disk(folder, photos)
                else:
                    gd_uploader.upload_ig_photos(folder, photos)
            else:
                print('неправильный ввод')
        elif social_network == 'exit' or storage == 'exit':
            print('завершение программы')
            break
        else:
            print('неправильный ввод')
