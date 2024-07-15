# Тестовое задание для Mycego

import os
import requests
from PIL import Image
from urllib.parse import urlencode


def create_temp(temp_dir):
    """Создание временной папки для загрузки фото."""
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

def delete_temp(temp_dir):
    """Удаление временной папки для загрузки фото.."""
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)
    
def get_resource_items(base_url_meta, public_key, path=None):
    """Получение вложенний в ресурсе."""
    if path:
        meta_data_url = base_url_meta + urlencode(dict(public_key=public_key, path=path))
    else:
        meta_data_url = base_url_meta + urlencode(dict(public_key=public_key))
    response = requests.get(meta_data_url)
    response.raise_for_status()
    return response.json()['_embedded']['items']

def get_href_download_photo(base_url_download, public_key, path):
        """Получение ссылки на скачивание фото."""
        download_url = base_url_download + urlencode(dict(public_key=public_key, path=path))
        download_response = requests.get(download_url)
        download_response.raise_for_status()
        return download_response.json()['href']

def download_photos(download_href, local_path, photo_name):
    """Загрузка фотографий."""
    download_response = requests.get(download_href)
    download_response.raise_for_status()
    with open(local_path, 'wb') as file:
        file.write(download_response.content)
    print(f'Загрузка фото: {photo_name}')

def create_tiff(image_folder, result_file):
    """Создание файла .tif"""
    images = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith('.png'):
            file_path = os.path.join(image_folder, filename)
            images.append(Image.open(file_path))
    if images:
        images[0].save(result_file, save_all=True, append_images=images[1:], compression='tiff_deflate')
    print(f'Файл {result_file} создан')

def main(required_dirs, result_file):
    base_url_meta = 'https://cloud-api.yandex.net/v1/disk/public/resources?' # основной путь получения метаинформации ресурса    
    base_url_download = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?' # основной путь загрузки ресурса    
    public_key = 'https://disk.yandex.ru/d/V47MEP5hZ3U1kg' # ссылка на ресурс    
    temp_dir = 'temp' # название временной папки

    if required_dirs:
        create_temp(temp_dir=temp_dir)

        # Проходимся по вложенным папкам ресурса
        for dir in get_resource_items(base_url_meta=base_url_meta, public_key=public_key):
            dir_name = dir['name']
            if dir_name in required_dirs:
                # получаем метаинформацию конкретной папки
                for photo in get_resource_items(base_url_meta=base_url_meta, public_key=public_key, path=dir['path']):
                    photo_name = photo['name']
                    download_href = get_href_download_photo(base_url_download=base_url_download, public_key=public_key, path=photo['path'])
                    full_photo_name = f'{dir_name}_{photo_name}' # имя фото с папкой
                    local_path = os.path.join(temp_dir, full_photo_name) # путь сохранения фото
                    download_photos(download_href=download_href, local_path=local_path, photo_name=full_photo_name)

        create_tiff(image_folder=temp_dir, result_file=result_file)

        delete_temp(temp_dir)

if __name__ == "__main__":
     # Список имен папок из которых нужно взять изображения
    required_dirs = [
        '1369_12_Наклейки 3-D_3',
        '1388_12_Наклейки 3-D_3',
        '1388_2_Наклейки 3-D_1',
        '1388_6_Наклейки 3-D_2',
    ]
    result_file = 'result.tif'
    main(required_dirs, result_file)
