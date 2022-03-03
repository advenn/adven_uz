import os
import subprocess
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import requests
import youtube_dl
import yt_dlp
from acrcloud.recognizer import ACRCloudRecognizer
from pydeezer import Deezer
from pydeezer.constants import track_formats

from data.config import ACR_HOST, ACR_ACCESS_KEY, ACR_SECRET_KEY, arl
# from data.config import ACR_HOST

# ACR_HOST
deezer = Deezer(arl=arl)
SPOTIFY_TRACK_LINK = 'https://open.spotify.com/track/'
YOUTUBE_LINK = 'https://youtu.be/'
youtube_urls = ['www.youtube.com', 'youtube.com', 'm.youtube.com', 'youtu.be']
tiktok_urls = ['tiktok.com', 'www.tiktok.com', 'm.tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com']
ydl = yt_dlp.YoutubeDL({'outtmpl': '%(id)s.%(ext)s', 'paths': {'home': os.path.join(os.getcwd(), 'media')}})
ytdl = youtube_dl.YoutubeDL(
    {'outtmpl': '%(id)s.%(ext)s', 'paths': {'home': os.path.join(os.getcwd(), 'media')}})
VIDEO_PATH = os.path.join(os.getcwd(), 'media')
MUSIC_PATH = os.path.join(os.getcwd(), 'media')
ACRCLOUD_ERROR_CODES = {'0': 'Recognition succeed', '1001': 'No recognition result',
                        '2000': 'Recording error (device may not have permission)',
                        '2001': 'Init failed or request timeout', '2002': 'Metadata parse error',
                        '2004': 'Unable to generate fingerprint', '2005': 'Timeout',
                        '3000': 'Recognition service error (http error 500)',
                        '3003': 'Limit exceeded, please upgrade your account', '3006': 'Invalid arguments',
                        '3014': 'Invalid signature', '3015': 'QpS limit exceeded, please upgrade your account'}


def extract_platform(url):
    data = {}
    if len(url) > 19:
        response = requests.get(url)
        parsed_url = urlparse(str(response.url))
        platform = parsed_url.netloc
        platform = '.'.join(platform.split('.')[-2:])
        if 'tiktok.com' in platform or ('youtube.com' in platform and 'shorts' in url):
            data['msg'] = 'success'
            data['platform'] = platform
        else:
            data['msg'] = 'fail'
            data['platform'] = platform
    else:
        data['msg'] = 'fail'
        data['platform'] = ''
    return data


def download_video_shorts(url):
    print('youtube initiated')
    # yt = YouTube(url)
    with ydl as downloader:
        video = downloader.extract_info(
            url=url,
            download=True
        )
        # print(video)
        details = {}
        video_id = video['id']
        title = video['title']
        thumb = video['thumbnail']
        description = video['description']
        details = {'video_id': video_id, 'thumb': thumb, 'title': title, 'description': description}
        try:
            artist = video['artist']
            details['artist'] = artist
        except KeyError:
            pass
        try:
            track = video['track']
            details['track'] = track
        except KeyError:
            pass
        try:
            album = video['album']
            details['album'] = album
        except KeyError:
            pass
        # try:
        #     extension = video['ext']
        #     filename = "{0}.{1}".format(video_id, extension)
        #     details['extension'] = extension
        #     details['filename'] = filename
        # except KeyError:
        files = pd.Series(np.array(os.listdir(VIDEO_PATH)))
        filename = files[files.str.startswith(video_id) & ~files.str.endswith('.mp3')].values[0]
        # if str(filename).endswith('.mp3')
        details['filename'] = filename
        full_path = os.path.join(os.getcwd(), 'media', filename)
        # yt.streams.get_highest_resolution().download()
        details['full_path'] = full_path
    return details


def download_video_tiktok(url):
    print('tiktok initiated')
    # video = api.get_tiktok_by_url(url)
    # video_details = video['itemInfo']['itemStruct']
    # video_id = video_details['id']
    # title = video['shareMeta']['title']
    # thumb = video_details['video']['originCover']
    # description = video['shareMeta']['desc']
    # extension = video_details['video']['format']
    # filename = "{}.{}".format(video_id, extension)
    # tiktok = api.get_video_by_tiktok(video)
    # full_path = os.path.join(VIDEO_PATH, filename)
    # with open(full_path, 'wb') as file:
    #     file.write(tiktok)
    # details = {'video_id': video_id, 'thumb': thumb, 'title': title, 'description': description,
    #            'full_path': full_path}
    with ydl as downloader:
        video = downloader.extract_info(
            url=url,
            download=False
        )
        # print(video)
        details = {}
        video_id = video['id']
        title = video['title']
        thumb = video['thumbnail']
        description = video['description']
        details['video_id'] = video_id
        details['thumb'] = thumb
        details['title'] = title
        details['description'] = description
        try:
            artist = video['artist']
            details['artist'] = artist
        except KeyError:
            pass
        try:
            track = video['track']
            details['track'] = track
        except KeyError:
            pass
        try:
            album = video['album']
            details['album'] = album
        except KeyError:
            pass
        try:
            extension = video['video_ext']
            filename = "{0}.{1}".format(video_id, extension)
            details['extension'] = extension
            details['filename'] = filename
        except KeyError:
            files = pd.Series(np.array(os.listdir(VIDEO_PATH)))
            filename = files[files.str.startswith(video_id)].values[0]
            details['filename'] = filename
        full_path = os.path.join(VIDEO_PATH, details['filename'])
        details['full_path'] = full_path
        return details
    # return details


acrconfig = {
    'host': ACR_HOST,
    'access_key': ACR_ACCESS_KEY,
    'access_secret': ACR_SECRET_KEY,
    'timeout': 10,
}

'''This module can recognize ACRCloud by most of audio/video file. 
    Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
    Video: mp4, mkv, wmv, flv, ts, avi ...'''
recognizer = ACRCloudRecognizer(acrconfig)


def recognize(path):
    """
{'cost_time': 0.015000104904175,
 'metadata': {'music': [{'acrid': 'd1f6aa66e2a15b162f7f788d2a30cef4',
                         'album': {'name': "Baby I'm Yours"},
                         'artists': [{'name': 'Breakbot'}],
                         'duration_ms': 215786,
                         'external_ids': {},
                         'external_metadata': {'spotify': {'album': {'name': 'Baby '
                                                                             "I'm "
                                                                             'Yours'},
                                                           'artists': [{'name': 'Breakbot'},
                                                                       {'name': 'Irfane'}],
                                                           'track': {'id': '46u45Dhe0ArF7CuPEi2Jxl',
                                                                     'name': 'Baby '
                                                                             "I'm "
                                                                             'Yours '
                                                                             '(feat. '
                                                                             'Irfane)'}},
                                               'youtube': {'vid': '6okxuiiHx2w'}},
                         'label': 'Ed Banger Records \\/ Because Music',
                         'play_offset_ms': 15520,
                         'release_date': '2013-07-22',
                         'result_from': 3,
                         'score': 100,
                         'title': "Baby I'm Yours (feat. Irfane)"}],
              'timestamp_utc': '2022-01-12 15:43:14'},
 'result_type': 0,
 'status': {'code': 0, 'msg': 'Success', 'version': '1.0'}}
"""
    recognized = eval(recognizer.recognize_by_file(path, 0))
    parsed = {}
    status_code = recognized['status']['code']
    parsed['code'] = status_code
    if status_code == 0:
        music_list = []
        music = recognized['metadata']['music']
        for i in music:
            music_details = {}
            album = i['album']['name']
            artists = ", ".join([j['name'] for j in i['artists']])
            music_details['album'] = album
            music_details['artists'] = artists
            if i['external_metadata']:
                try:
                    # i['external_metadata']['spotify']:
                    music_details['spotify'] = i['external_metadata']['spotify']
                    # music_details['spotify']['artists']['name']
                    names = ", ".join([sh['name'] for sh in i['external_metadata']['spotify']['artists']])
                    music_details['spotify']['artists'] = {'name': names}
                    # for key, value in i['external_metadata']['spotify'].items():
                    #     spotify={}
                    #     spotify[key] = ", ".join([ for k in value.keys()])
                    spotify_link = SPOTIFY_TRACK_LINK + i['external_metadata']['spotify']['track']['id']
                    music_details['spotify_link'] = spotify_link
                except KeyError:
                    pass
                    # spotify_link = None
                    # music_details['spotify_link'] = spotify_link
                try:
                    # i['external_metadata']['youtube'] :
                    music_details['youtube'] = i['external_metadata']['youtube']
                    youtube_link = YOUTUBE_LINK + i['external_metadata']['youtube']['vid']
                    music_details['youtube_link'] = youtube_link
                except KeyError:
                    pass
                    # youtube_link = None
                    # music_details['youtube_link'] = youtube_link
            try:
                # i['title']:
                music_details['title'] = i['title']
            except KeyError:
                pass
                # music_details['title'] = None
            music_list.append(music_details)
        parsed['parsed'] = music_list
        parsed['msg'] = recognized['status']['msg']
    else:
        parsed['msg'] = recognized['status']['msg']
    return parsed


def video_convertor(filename):
    FNULL = open(os.devnull, 'w')
    com = """ffmpeg -i {0} -codec copy -strict -2 {1}.mp4 -y""".format(filename, filename.split('.')[0]).split()
    result = subprocess.call(com, stdout=FNULL,
                             stderr=subprocess.STDOUT)

    if int(result) == 0:
        # os.remove(filename)
        return filename.split('.')[0] + '.mp4'
    else:
        return filename


def video2audio(filename):
    FNULL = open(os.devnull, 'w')
    com = """ffmpeg -i {0} {1}.mp3 -y""".format(filename, filename.split('.')[0]).split()
    result = subprocess.call(com, stdout=FNULL,
                             stderr=subprocess.STDOUT)
    if int(result) == 0:
        return filename.split('.')[0] + '.mp3'
    else:
        return filename


def search_n_download_music(query):
    # query = f"{details['title']['name']}  {details['artists']['name']}"
    # results = deezer.search_tracks(query, limit=1)
    track_search_results = deezer.search_tracks(query, limit=1)
    if len(track_search_results) > 0:
        track_id = track_search_results[0]['id']
        track = deezer.get_track(track_id)
        track_info = track['info']
        lyrics = ''
        try:
            lyrics = track_info['LYRICS']['LYRICS_TEXT']
        except Exception:
            lyrics = ''
        track_title = track_info['DATA']['SNG_TITLE']
        filename = f'{track_title}.mp3'
        track['download'](MUSIC_PATH, quality=track_formats.MP3_320, filename=filename)
        # files = os.listdir('media/music')
        # df = pd.Series(files)
        # files = pd.Series(np.array(os.listdir(MUSIC_PATH)))
        # filename = files[files.str.startswith(track_title) & files.str.endswith('.mp3')].values[0]
        # filename = df.str
        # for i in files:
        #     if track_title in i and not i.endswith('.lrc'):
        #         filename = i
        return {'msg': 'success', 'lyrics': lyrics, 'track_title': track_title, 'filename': filename}
    else:
        return {'msg': 'fail'}
    # return results
