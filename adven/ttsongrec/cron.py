import os
import time
from pathlib import Path

import pandas as pd
import telebot

bot = telebot.TeleBot('5219654706:AAGYCTr3svIKh92opj90IWzf-gv9PTT9u_M')
media_path = Path(__file__).resolve().parent.parent / 'media'
print(media_path)
ADMIN_TG_ID = 341598437


def get_information(directory):
    file_list = []
    for i in os.listdir(directory):
        a = os.stat(os.path.join(directory, i))
        file_list.append(
            [i, time.ctime(a.st_atime), a.st_atime, time.ctime(a.st_ctime)])  # [file,most_recent_access,created]
    return file_list


def get_15min(files: list):
    df = pd.DataFrame(data=files, columns=['name', 'accessed_at', 'access', 'created_at'])
    current_time = time.time()
    older_files = df[df.access < (current_time - 900)]
    deleted = 0
    for index, name in older_files.name.iteritems():
        os.remove(media_path / name)
        # print(name)
        deleted += 0
    bot.send_message(chat_id=ADMIN_TG_ID, text=f"[DELETED]: {deleted} files, from {df.shape[0]}")
    return deleted


def my_cron_job():
    files = get_information(media_path)
    print(files)
    get_15min(files)
    return

