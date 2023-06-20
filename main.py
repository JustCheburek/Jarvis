# Встроенные библиотеки
import os
import random
import struct
import subprocess
import sys
import time
from ctypes import POINTER, cast
from threading import Thread

import pip


# Принты
def install_library(library, color=True):
    if color:
        print(f"[green]Установка библиотеки[/green] [red]{library}[/red]")
    else:
        print(f"Установка библиотеки {library}")
    pip.main(['install', library])


def uninstall_library(library):
    print(f"[green]Удаление библиотеки[/green] [red]{library}[/red]")
    try:
        pip.main(['uninstall', library])
    except:
        pass


def error_print(message):
    print(f"[[dark_red]Error[/dark_red]] [red]{message}[/red]")


def warn_print(message):
    print(f"[[orange]Warning[/orange]] [yellow]{message}[/yellow]")


def log_print(message):
    print(f"[[green]Log[/green]] [green]{message}[/green]")


def bot_print(message):
    print(f"[[green]{config.ALIASES[1]}[/green]] [green]{message}[/green]")


# Библиотеки
try:
    from rich import print
except ImportError:
    install_library('rich', color=False)
    from rich import print

try:
    import pvporcupine
except ImportError:
    install_library('pvporcupine')
    import pvporcupine

try:
    import vosk
except ImportError:
    install_library('vosk')
    import vosk

try:
    import yaml
except ImportError:
    install_library('PyYAML')
    import yaml

try:
    from comtypes import CLSCTX_ALL
except ImportError:
    install_library('comtypes')
    from comtypes import CLSCTX_ALL

try:
    from fuzzywuzzy import fuzz
except ImportError:
    install_library('fuzzywuzzy')
    from fuzzywuzzy import fuzz

try:
    from gpt4free import usesless
except ImportError:
    install_library('gpt4free')
    from gpt4free import usesless

try:
    from pvrecorder import PvRecorder
except ImportError:
    install_library('pvrecorder')
    from pvrecorder import PvRecorder

try:
    from pycaw.pycaw import (
        AudioUtilities,
        IAudioEndpointVolume
    )
except ImportError:
    install_library('pycaw')
    from pycaw.pycaw import (
        AudioUtilities,
        IAudioEndpointVolume
    )

try:
    from speakerpy import lib_speak
    from speakerpy import lib_sl_text
except ImportError:
    install_library('speakerpy')
    from speakerpy import lib_speak
    from speakerpy import lib_sl_text

try:
    import discord
except ImportError:
    uninstall_library('discord.py')
    install_library('py-cord')
    import discord

try:
    import nacl.utils
except:
    install_library('PyNaCl')
    import nacl.utils

try:
    from playsound import playsound
except:
    install_library('playsound==1.2.2')
    from playsound import playsound

try:
    import asyncio
except:
    install_library('asyncio')
    import asyncio

try:
    import webbrowser
except:
    install_library('webbrowser')
    import webbrowser

try:
    import simplejson as json
except:
    install_library('simplejson')
    import simplejson as json

try:
    import win32api
except:
    install_library('pywin32')
    import win32api

try:
    from dotenv import load_dotenv
except:
    install_library('python-dotenv')
    from dotenv import load_dotenv

try:
    import Levenshtein
except:
    install_library('python-Levenshtein')
    import Levenshtein


# Файловые библиотеки
import config
from config import settings

# Переменные Джарвиса
# Команды
CMD_LIST = yaml.safe_load(
    open('commands.yaml', 'rt', encoding='utf8'),
)
# Токены
tokens = load_dotenv('tokens.env')

# PORCUPINE
porcupine = pvporcupine.create(
    access_key=os.environ.get("PICOVOICE_TOKEN"),
    keywords=['jarvis'],
    sensitivities=[1]
)

# VOSK
model = vosk.Model("model_small")
samplerate = 16000
device = settings["micro"]["index"]
kaldi_rec = vosk.KaldiRecognizer(model, samplerate)

# Discord
intents = discord.Intents().all()
bot = discord.Bot(intents=intents)
vc = None

# Запись голоса
recorder = PvRecorder(device_index=settings["micro"]["index"], frame_length=porcupine.frame_length)
recorder.start()
print(f'[green]Использую девайс[/green]: [red]{recorder.selected_device}[/red]')
log_print('Запись включена')

# Текст в голос
speaker = lib_speak.Speaker(model_id="v3_1_ru", language="ru", speaker='aidar', device="cpu")


# Дс функции
@bot.event
async def on_ready():
    global vc

    log_print(f'Бот запущен, как {bot.user}')

    await join_user()


@bot.command()
async def join(ctx):
    global vc

    user = ctx.author
    voice = user.voice
    voice_channel = voice.channel

    if not voice:
        return await ctx.respond("Вы не в войсе!")

    try:
        vc = await voice_channel.connect()
        await ctx.respond(f"Присоединяюсь к голосовому каналу {voice_channel}")
        play("greet")

    except discord.errors.ClientException:
        say(text="Проверьте консоль")
        warn_print("Бот уже находится в голосовом канале")
        await ctx.respond("Я в голосовом канале")


async def join_user():
    global vc

    guild = bot.get_guild(settings["ds"]["ds_guild"])
    user = bot.get_user(settings["ds"]["ds_id"])
    all_channels = bot.get_all_channels()

    if user is None:
        error_print("Дс айди неверен! (ну или недостаточно прав для просмотра юзеров)")
        return

    for channel in all_channels:
        if channel.type == discord.ChannelType.voice:
            voice_channel = bot.get_channel(channel.id)
            if user in voice_channel.members:
                break
    else:
        voice_channel = None

    vc = discord.utils.get(bot.voice_clients, guild=guild)

    if vc is not None:
        play("greet")

    elif voice_channel is not None:
        vc = await voice_channel.connect()
        play("greet")


def say(text="", filename=None):
    global speaker, vc

    if not settings["sound"]["ds"]:
        if text != "":
            speaker.speak(
                text=text,
                sample_rate=48000,
                speed=settings["sound"]["speed"]
            )

        elif filename is not None:
            playsound(filename)

    else:
        if text != "":
            name = "speech"
            for file in os.listdir(config.SPEECH_PATH):
                if file.endswith(".mp3"):
                    os.remove(f"{config.SPEECH_PATH}/{file}")

            speaker.to_mp3(
                text=text,
                sample_rate=48000,
                audio_dir=config.SPEECH_PATH,
                name_text=config.SPEECH_PATH,
                speed=settings["sound"]["speed"]
            )

            for file in os.listdir(config.SPEECH_PATH):
                if file.endswith(".mp3"):
                    filename = f"{config.SPEECH_PATH}/{file}"
                    break

        if vc is None:
            vc = discord.utils.get(bot.voice_clients, guild=bot.get_guild(settings["ds"]["ds_guild"]))

        if vc is not None:
            try:
                vc.play(
                    source=discord.FFmpegPCMAudio(filename)
                )
                return
            except:
                pass

        warn_print("Дискорд бот не в голосовом канале")
        playsound(filename)


def gpt_answer(text):
    try:
        response = usesless.Completion.create(
            systemMessage=f"Ты, помощник {config.ALIASES[0]}",
            prompt=text,
            temperature=0.4,
            parentMessageId=settings["gpt_id"]
        )

        settings["gpt_id"] = response["id"]
        config.update_user_info()
        return response["text"]
    except:
        pass

    return None


def play(phrase):
    sound_files = os.listdir(config.SOUND_PATH)

    sounds = []

    for sound in sound_files:
        if sound.startswith(phrase) and sound.endswith(f'.wav'):
            sounds.append(sound)

    if len(sounds) > 0:
        filename = os.path.join(config.SOUND_PATH, random.choice(sounds))

        say(filename=filename)

    else:
        error_print(f'Звук "{phrase}" не найден')


def respond(voice: str):
    global recorder

    cmd = cmd_get_ready(voice)

    print(f"[green]Распознано[/green]: [red]{voice}[/red]")

    if voice in config.ALIASES:
        recorder.stop()
        log_print('Запись приостановлена')
        play("greet")
        bot_print("Я уже слушаю тебя")
        recorder.start()
        log_print('Запись включена')
        return True

    if len(cmd['cmd'].strip()) <= 0:
        return False

    log_print(f'Команда - [red]{cmd["cmd"]}[/red], вероятность - [red]{cmd["percent"]}[/red]')

    recorder.stop()
    log_print('Запись приостановлена')

    if cmd['percent'] >= 70 and cmd['cmd'] in CMD_LIST:
        execute_cmd(cmd['cmd'], voice)

    else:
        for phrase in config.TBR:
            len_words = len(phrase.split(" "))
            first_words = voice.join(voice.split(" ")[:len_words]).strip()

            if fuzz.ratio(first_words, phrase) > 75:
                response = gpt_answer(voice)
                if response is not None:
                    say(text=response)
                else:
                    warn_print(
                        "Бесплатные попытки у ChatGPT закончились на сегодня"
                    )

                break

        else:
            warn_print(f'Кажется вы не сказали вводную фразу в начале предложения:\n {", ".join(config.TBR)}')

    time.sleep(0.5)
    recorder.start()
    log_print('Запись включена')

    if "спасибо" in voice or \
            "окей" in voice or \
            "ок" in voice:
        return False
    else:
        return True


def cmd_get_ready(cmd: str):
    for alias in config.ALIASES:
        cmd = cmd.replace(alias, "").strip()

    for tbr in config.TBR:
        cmd = cmd.replace(tbr, "").strip()

    rc = {
        'cmd': '',
        'percent': 0
    }

    for command, list_phrases in CMD_LIST.items():
        for phrase in list_phrases:
            percent = fuzz.ratio(cmd, phrase)
            if percent > rc['percent']:
                rc['cmd'] = command
                rc['percent'] = percent

    return rc


def execute_cmd(cmd: str, text: str):
    if cmd == 'browser':
        play("ok")
        webbrowser.open(config.MINEBRIDGE_URL)

        return

    elif cmd == 'sound_on':
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(0, None)

        play("ok")

        return

    elif cmd == 'sound_off':
        play("ok")

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1, None)

        return

    elif cmd == 'thanks' or cmd == 'stupid':
        play(cmd)
        return

    elif cmd == "join_ds" and settings["sound"]["ds"]:
        asyncio.run(join_user())
        return

    elif cmd == "repeat":
        say(text=text.split(" ")[3:])
        return

    elif cmd == 'off':
        play("off")

        # Выход
        sys.exit()

    log_print(f"Самодельная команда - {cmd}")
    user_file = f"{cmd}.txt"

    # По очереди проверяем в каждой папке команду
    for path_dir_commands in tuple(config.COMMANDS):  # commands/тип команды
        # Получаем полный путь к файлу
        path_command = os.path.join(path_dir_commands, user_file)

        # Открываем папку команд и смотрим содержимое
        user_command_files = os.listdir(path_dir_commands)

        # Проверяем есть ли данная команда в списке команд
        if user_file in user_command_files and os.path.isfile(path_command):
            # Открываем .txt файл и смотрим путь / ссылку
            with open(path_command, "r", encoding="utf-8") as file:
                user_command = file.read()
                file.close()

            try:
                result = config.COMMANDS[path_dir_commands](user_command, path_command)

                # Говорим
                play(result["say"])

            except Exception as e:
                error_print(e)

            return

    user_file = f"{cmd}.exe"

    # Получаем полный путь к файлу
    path_command = os.path.join(config.COMMANDS_PATH, user_file)

    if os.path.isfile(path_command):
        subprocess.Popen([path_command])
        return

    error_print("Созданная вами команда не была распознана")


def run_bot():
    global recorder, ltc

    log_print(f"{config.ALIASES[1]} начал свою работу ...")
    play("run")
    time.sleep(0.4)

    cache = os.path.join(config.SPEECH_PATH, "cache")

    if os.path.isdir(cache):
        cache_files = os.listdir(cache)
        for file in cache_files:
            os.remove(os.path.join(cache, file))

    ltc = time.time()

    while True:
        try:
            pcm = recorder.read()
            keyword_index = porcupine.process(pcm)

            # Первая фраза
            if keyword_index >= 0:
                recorder.stop()
                log_print('Запись приостановлена')
                play("greet")
                bot_print("Привет")
                recorder.start()
                log_print('Запись включена')
                ltc = time.time()

            # Продолжение
            while time.time() - ltc <= settings["sound"]["wait_with_no_wake_word"]:
                pcm = recorder.read()
                sp = struct.pack("h" * len(pcm), *pcm)

                if kaldi_rec.AcceptWaveform(sp):
                    if respond(json.loads(kaldi_rec.Result())["text"]):
                        ltc = time.time()

                    break

        except Exception as err:
            error_print(f"{err=}")
            recorder.start()


def run_ds_bot():
    bot.run(os.environ.get("DS_TOKEN"))


# Одновременный запуск двух процессов
run_bot = Thread(target=run_bot)
run_bot.start()

if settings["sound"]["ds"]:
    run_ds_bot = Thread(target=run_ds_bot)
    run_ds_bot.start()
    run_ds_bot.join()

run_bot.join()
