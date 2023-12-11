import requests
import zipfile
import os

def download_file(url, file_name):
    # Удаляем старый файл перед скачиванием, если он существует
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"Удален старый файл {file_name}.")

    # Загружаем файл
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Файл {file_name} успешно загружен.")
    else:
        print("Ошибка при загрузке файла.")

def extract_zip(zip_file):
    # Проверяем наличие ZIP-файла
    if os.path.exists(zip_file):
        # Распаковываем ZIP-файл
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall()
        print(f"Файл {zip_file} успешно распакован.")
    else:
        print("Файл не найден.")

def remove_folders(directory):
    # Получаем список всех папок внутри директории
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        # Условие для проверки подстроки в названии файла
    condition = lambda file: 'v1.1' in file or 'mean' in file

        # Удаляем файлы, удовлетворяющие условию
    for file in files:
        if condition(file):
            file_path = os.path.join(directory, file)
                # Удаляем файл
            os.remove(file_path)
            #print(f'Файл {file_path} удален.')

def load_all_data():
    # Пример использования функций:
    url = "http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=2fa2eefd-01b5-41a7-802e-66ca6d0a5087%20&output=zip.zipgroup"
    file_name = "data.zip"
    zip_file = "data.zip"
    directory = './SLAM/'

    # Скачиваем файл
    download_file(url, file_name)

    # Распаковываем ZIP-файл
    extract_zip(zip_file)

    # Удаляем определенные папки
    remove_folders(directory)

    print('Процесс скачивания данных закончен')
    
    