import os
import subprocess
import webbrowser

import simplejson as json
import win32api

user_info = "user_info.json"


def get_user_info():
    """
    Получение информации из json файла
    """
    with open(user_info, "r") as file:
        info = json.load(
            file,
            encoding="utf-8"
        )
        return info


def send_user_info(info):
    """
    Получение информации из json файла
    """
    with open(user_info, "w") as file:
        json.dump(
            info,
            file,
            encoding="utf-8",
            ensure_ascii=False
        )


# Самостоятельные команды
def open_exe(path, user_file):
    """
    Открывает файл по его абсолютному пути

    :param str path: содержимое команды в файле .txt
    :param str user_file: путь до файла .txt

    :return: {"say": "ответ бота"}
    """

    if os.path.isfile(path):
        subprocess.Popen([path])
    else:
        all_places = find_file_in_all_drives(path)
        print("\n".join(all_places))

        if len(all_places) > 1:
            while True:
                path = int(input(f"Выберете путь (1-{len(all_places)}): "))
                if 1 <= path <= len(all_places):
                    path = all_places[path - 1]
                    break

        with open(user_file, "w", encoding="utf-8") as file:
            file.write(path)
            file.close()

        subprocess.Popen([path])

    return {
        "say": "ok"
    }


def close_exe(name_file, _):
    """
    Закрывает файл по его названию

    :param str name_file: содержимое команды в файле .txt
    :param str _: путь до файла .txt

    :return: {"say": "ответ бота"}
    """

    subprocess.call(["taskkill", "/F", "/IM", name_file])
    return {
        "say": "ok"
    }


def open_url(url, _):
    """
    Открывает ссылку

    :param str url: содержимое команды в файле .txt
    :param str _: путь до файла .txt

    :return: {"say": "ответ бота"}
    """

    webbrowser.open(url)
    return {
        "say": "ok"
    }


def find_file_in_all_drives(file_name):
    print(f"Начинается поиск - {file_name}")
    all_places = []

    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        for root, _, files in os.walk(drive):
            for f in files:
                if file_name.lower() == f.lower() and "$Recycle.Bin" not in root:
                    all_places.append(os.path.join(root, f))

    return all_places
