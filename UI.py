from vk_api import VkUser
from Odnoklassniki_API import OkApi
from YaUploader import YaUploader


def user_interface():
    while True:
        print('Выберите соцсеть: 1 - VK, 2 - Odnoklassniki, "exit" - выход')
        social_network = input()
        if social_network == '1':
            user_id = int(input('Введите id пользователя:'))
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
                photos = vk_client.get_photos(user_id=user_id, album_id='wall')
                uploader.upload_photos_to_disk(folder, photos)
            elif option == 2:
                photos = vk_client.get_photos(user_id=user_id, album_id='saved')
                uploader.upload_photos_to_disk(folder, photos)
            elif option == 3:
                photos = vk_client.get_photos(user_id=user_id)
                uploader.upload_photos_to_disk(folder, photos)
            elif option == 4:
                photos = vk_client.get_albums_photos(user_id=user_id)
                uploader.upload_photos_to_disk(folder, photos)
            else:
                print('неправильный ввод')
        elif social_network == '2':
            user_id = input('Введите id пользователя:')
            folder = input('введите название папки:')
            print('''
            откуда скачиваем фото?
            1 - аватарки;
            2 - фото из альбомов;
            ''')
            option = int(input())
            if option == 1:
                photos = ok_loader.get_user_photos(user_id)
                uploader.upload_photos_to_disk(folder, photos)
            elif option == 2:
                albums_list = ok_loader.get_user_albums(user_id)
                photos = ok_loader.get_albums_photos(albums_list)
                uploader.upload_photos_to_disk(folder, photos)
            else:
                print('неправильный ввод')
        elif social_network == 'exit':
            print('завершение программы')
            break
        else:
            print('неправильный ввод')


if __name__ == '__main__':
    VK_TOKEN = ''
    YA_TOKEN = ''
    OK_TOKEN = ''
    OK_APP_KEY = ''
    OK_SSK = ''
    uploader = YaUploader(YA_TOKEN)
    vk_client = VkUser(VK_TOKEN, '5.131')
    ok_loader = OkApi(OK_TOKEN, OK_SSK, OK_APP_KEY)
    user_interface()
