import os
import subprocess
import webbrowser

import simplejson as json
import win32api
from rich import print

user_info = "user_info.json"


# Инфо о юзере
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
    Открывает файл по его абсолютному пути, если же этот путь неверен, он будет искать приложение сам

    :param str path: содержимое команды в файле .txt
    :param str user_file: путь до файла .txt

    :return: {"say": "ответ бота"}
    """

    if os.path.isfile(path):
        subprocess.Popen([path])
    else:
        if "\\" in path:
            warn_print(f"Файл по пути {path} не был найден! Начинаю самостоятельный поиск")

            file = path.split("\\")[-1:][0]

        else:
            file = path

        all_places = find_file(file)

        if len(all_places) > 0:
            if len(all_places) > 1:
                while True:
                    path = int(input(f"Выберете путь (1-{len(all_places)}): "))
                    if 1 <= path <= len(all_places):
                        path = all_places[path - 1]
                        break
            else:
                path = all_places[0]

            log_print(f"Сохраняю новый путь - {path}")

            with open(user_file, "w", encoding="utf-8") as file:
                file.write(path)
                file.close()

            subprocess.Popen([path])

        else:
            error_print(f"Приложение {file} не было найдено! Вы точно правильно ввели название?")

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


def find_file(file_name):
    """
    Поиск файла во всех местах

    :param str file_name: имя файла

    :return: список путей
    """

    log_print(f"Начинается поиск - {file_name}")
    all_places = []

    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        for root, _, files in os.walk(drive):
            for f in files:
                if file_name.lower() == f.lower() and "$Recycle.Bin" not in root:
                    all_places.append(os.path.join(root, f))
                    log_print(f"Найден путь - {os.path.join(root, f)}")

    return all_places


def check_elems_in_text(text, elems: tuple):
    """
    Проверка текста на наличие в нем указанных элементов

    :param str text: текст
    :param tuple elems: элементы

    :return: boolean
    """

    for elem in elems:
        if elem in text:
            return elem

    return None


def error_print(message):
    print(f"[[dark_red]Error[/dark_red]] [red]{message}[/red]")


def warn_print(message):
    print(f"[[yellow]Warning[/yellow]] [yellow]{message}[/yellow]")


def log_print(message):
    print(f"[[green]Log[/green]] [green]{message}[/green]")


def bot_print(message):
    print(f"[[green]Jarvis[/green]] [green]{message}[/green]")
