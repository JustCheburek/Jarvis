import funcs

settings = funcs.get_user_info()


def update_user_info():
    """
    Обновления информации
    """
    funcs.send_user_info(settings)


# Пути
COMMANDS_PATH = "commands"
SOUND_PATH = "sound"
SPEECH = "speech"
SPEECH_PATH = f"{SOUND_PATH}/{SPEECH}"

# Самостоятельные команды
COMMANDS = {
    f"{COMMANDS_PATH}/open_exe": funcs.open_exe,
    f"{COMMANDS_PATH}/close_exe": funcs.close_exe,
    f"{COMMANDS_PATH}/open_url": funcs.open_url
}

# НЕ ИЗМЕНЯТЬ
# Бот-ассистент
ALIASES = ('джарвис', 'Jarvis')  # обращение: 1-ое как называют, 2-ое как пишется в консоли
TBR = ('скажи', 'расскажи', 'слушай')

# Ссылки
MINEBRIDGE_URL = "https://minebridge.ml"

if __name__ == "__main__":
    def need_answer(
            text: str,
            s: bool = True,
            default="",
            y_n: bool = False,
            type_answer=str
    ):
        """
        :param str text: отображаемый текст
        :param bool s: будет ли скип
        :param default: обычное значение, если будет скип (обязательно при s)
        :param bool y_n: да / нет
        :param type_answer: type ответа

        :return: input / default
        """

        answer = ""

        if not s and not y_n:
            while True:
                try:
                    return type_answer(input(text))
                except:
                    pass

        elif s and not y_n:
            while True:
                answer = input(text)

                if answer == "s":
                    return default

                try:
                    return type_answer(answer)
                except:
                    pass

        else:
            transform = {
                "y": True,
                "n": False,
                "s": default
            }

            while answer not in transform:
                answer = input(text)

            return transform[answer]


    print(
        "Изменения системных настроек!\n\n"
        "y - да\n"
        "n - нет\n"
        "s - скип (если есть дефолт)\n"
    )

    print("Личные данные\n")
    settings["user"]["name"] = need_answer(
        f'Введите свой позывало (сейчас - {settings["user"]["name"]}): ',
        s=False
    )
    settings["user"]["ds_id"] = need_answer(
        f'Введите свой дс айди (сейчас - {settings["user"]["ds_id"]}): ',
        s=False,
        type_answer=float
    )

    print("\nЗвук\n")
    settings["sound"]["speed"] = need_answer(
        "Введите скорость разговора (дефолт 1.3): ",
        default=1.3,
        type_answer=float
    )
    settings["sound"]["wait_with_no_wake_word"] = need_answer(
        "Введите сколько секунд бот будет ожидать без вводного слова Джарвис (дефолт 8): ",
        default=8,
        type_answer=int
    )
    settings["sound"]["ds"] = need_answer(
        "Введите будет ли идти звук из дс (y / n | нужен FFmpeg): ",
        default=False,
        y_n=True
    )

    print("\nМикро\n")
    settings["micro"]["ds"] = need_answer(
        "Выберите индекс микрофона (дефолт -1 (микро по умол)): ",
        default=-1,
        type_answer=int
    )

    update_user_info()
