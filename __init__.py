from vasisualy.skills.vas_skill.vas_skill import Skill  # Импорт родительского класса навыков.
import requests
from bs4 import BeautifulSoup
import random
import tempfile
import subprocess
import os
import platform
import wget


class Picture(Skill):
    def get_picture_url(self):
        site = requests.get("https://commons.wikimedia.org/wiki/Main_Page")  # Получение страницы WikiMedia.
        bs = BeautifulSoup(site.text, "html.parser")

        for link in bs.find_all("img"):
            image_url = link.get("src")
            break

        url_parts = image_url.split('/')
        url_parts.pop()
        url_parts.remove("thumb")
        image_url = ''

        for i in url_parts:
            image_url += i + '/'

        return image_url[:-1]

    def download_picture(self):
        url = self.get_picture_url()
        tmp = tempfile.gettempdir()  # Директория для временных файлов.

        r = requests.get(url)

        if platform.system() == "Windows":
            if "daily-image.png" in os.listdir(tmp):
                os.remove(f"{tmp}\\daily-image.png")
            wget.download(url, out=f"{tmp}\\daily-image.png")  # Загрузка изображения.
        else:
            if "daily-image.png" in os.listdir(tmp):
                os.remove(f"{tmp}/daily-image.png")
            wget.download(url, out=f"{tmp}/daily-image.png")

    def main(self, user_message):
        if super(Picture, self)._is_triggered(user_message, super(Picture, self)._get_triggers()):
            try:
                self.download_picture()
                if platform.system() == "Windows":
                    image = f"{tempfile.gettempdir()}\\daily-image.png"
                else:
                    image = f"{tempfile.gettempdir()}/daily-image.png"

                if platform.system() == "Windows":   # Команда запуска для Windows.
                    os.startfile(image)
                elif platform.system() == "Darwin":  # Команда запуска для Mac OS.
                    subprocess.Popen(["open", image])
                else:                                # Команда запуска для остальных систем (GNU/Linux, BSD, etc.).
                    subprocess.Popen(["xdg-open", image])

                toSpeak = "Открываю изображение..."
            except ConnectionError:
                toSpeak = "Нет подключения к сети..."
            return toSpeak
        else:
            return ''

def main(user_message):
    skill = Picture("picture_of_the_day", user_message)  # Вывод сообщения, переданного навыком, пользователю.
    return skill.main(user_message)
