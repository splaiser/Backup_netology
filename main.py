import requests
from requests import request
from pprint import pprint
import json
from datetime import datetime


class VKDOWLOADER:

    def __init__(self, token: str):
        self.token = token
        self.photo_list = []

    def get_photo_list(self):
        URL = "https://api.vk.com/method/photos.get"
        params = {
            "count": 100,
            "access_token": vk_TOKEN,
            "album_id": 'profile',
            "extended": '1',
            "photo_sizes": '1',
            "v": '5.131'
        }
        res = requests.get(URL, params=params)
        return res.json()

    # date = datetime.utcfromtimestamp(item.get('date')).strftime('%Y-%m-%d')

    def get_photo(self):
        dict = self.get_photo_list()
        items = (dict.get('response')).get('items')
        for item in items:
            photo_dict = {}
            photo_dict['filename'] = f"{(item.get('likes')).get('count')}.jpeg"
            photo_dict['photo'] = ((item.get('sizes'))[-1]).get('url')
            self.photo_list.append(photo_dict)
        return self.photo_list


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            "Contens-Type": 'application/json',
            "Authorization": f'OAuth {self.token}'
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):

        href_dict = self._get_upload_link(disk_file_path=disk_file_path)
        href = href_dict.get("href", "")
        photo_href = requests.get(filename.get('photo'))
        response = requests.put(href, data=photo_href)
        response.raise_for_status()
        if response.status_code == 201:
            print(f"Фотография {filename.get('filename')} загруженна.")

    def create_folder(self, folder_name):

        url = f"https://cloud-api.yandex.net/v1/disk/resources?path={folder_name}"
        headers = self.get_headers()
        response = requests.put(url=url, headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            print(f"Папка {folder_name} создана.")


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    vk_TOKEN = input("Введите ваш VK токен:")
    ya_TOKEN = input("Введите ваш Яндекс токен:")
    folder_name = input("Введите название папки куда поместить фотографии:")
    # vk_TOKEN = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"  # Введите VK токкен
    # ya_TOKEN = "AQAAAAABgt4oAADLW91g_cXfDEKziGeFEglOoxo"  # Введите YA токкен
    # folder_name = "netology"  # Введите название папки
    downloader = VKDOWLOADER(vk_TOKEN)
    uploader = YaUploader(ya_TOKEN)
    uploader.create_folder(folder_name)
    list = downloader.get_photo()
    for photo in list:
        path_to_file = f"{folder_name}/{photo.get('filename')}"
        uploader.upload_file_to_disk(path_to_file, photo)
