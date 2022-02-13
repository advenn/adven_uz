import mimetypes
import os

from colorama import init
from django.http import HttpResponse
from django.shortcuts import render, redirect

from adven.settings import STATIC_URL, BASE_DIR
from .forms import LinkForm
from .models import URL, Video, Music
# Create your views here.
from .utils import extract_platform, download_video_shorts, download_video_tiktok, recognize, video_convertor, \
    video2audio, search_n_download_music

GOOGLE_QUERY = 'https://www.google.com/search?q='
init()


def homepage(request):
    form = LinkForm()
    context = {'title': "Home", 'form': form}
    return render(request, template_name='main.html', context=context)


def recognizer(request):
    context = {'title': "Recognizing"}
    return render(request, template_name='recognizing.html', context=context)


def get_link(request):
    # print(1, request)
    # global platform_short_name
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            # print(2, form)
            # print(4,form.data)
            query_dict = form.data
            dict_query_dict = query_dict.dict()
            link = dict_query_dict['link']
            print(link)
            platform = extract_platform(link)
            if platform['msg'] == 'success':
                print(platform)
                details = {}
                if platform['platform'].lower() == 'youtube.com':
                    platform_short_name = 'yt'
                    url = URL()
                    url.url = link
                    url.platform_long = platform['platform']
                    url.platform_short = platform_short_name
                    url.save()
                    details = download_video_shorts(link)
                elif platform['platform'].lower() == 'tiktok.com':
                    platform_short_name = 'tt'
                    url = URL()
                    url.url = link
                    url.platform_long = platform['platform']
                    url.platform_short = platform_short_name
                    url.save()
                    details = download_video_tiktok(link)
                else:
                    return render(request, template_name='error.html',
                                  context={"title": "Error", 'code': 404, 'err': 'Unsupported platform'})

                # print(Fore.GREEN + str(details))
                video = Video()
                video.video_id = details['video_id']
                video.url = url
                video.title = details['title']
                video.thumb = details['thumb']
                video.description = details['description']
                mimetype = mimetypes.types_map['.{}'.format(details['filename'].split('.')[-1])]
                # print(Fore.RED + str(mimetype))
                if mimetype != mimetypes.types_map['.mp4']:
                    converted_video = video_convertor('static/video/' + details['filename'])
                    video.video = converted_video.split('/')[-1]
                    mimetype = mimetypes.types_map['.mp4']
                else:
                    video.video = os.path.join('video', details['filename'])
                video.save()
                file = os.path.join('static', 'video', str(video.video).split('/')[-1])
                # print(file)
                mp3file = video2audio(file)
                # print(mp3file)
                recognized = recognize(mp3file)
                # print(Fore.LIGHTGREEN_EX + str(recognized))
                if recognized['code'] == 0:
                    songs = recognized['parsed']
                    parsed = []
                    for song in songs:
                        music = Music()
                        music.name = song['title']
                        music.artist = song['artists']
                        music.save()
                        m = Music.objects.filter(artist=song['artists'], name=song['title'])[0]
                        music_id = m.pk
                        song['pk'] = music_id
                        # try:
                        #     del song['youtube']
                        # except:
                        #     pass
                        parsed.append(song)
                        # print(Fore.RED + str(parsed))
                    return render(request, "video.html",
                                  {"vidtitle": video.title,
                                   "image": details["thumb"],
                                   "title": video.title + " - Adven.uz",
                                   "STATIC_URL": STATIC_URL,
                                   "file": str(video.video).split('/')[-1],
                                   "mime_type": mimetype,
                                   # "music": parsed,
                                   "parsed": parsed})
                else:
                    return render(request, "video.html",
                                  {"vidtitle": video.title,
                                   "image": details["thumb"],
                                   "title": video.title + " - Adven.uz",
                                   "STATIC_URL": STATIC_URL,
                                   "file": str(video.video).split('/')[-1],
                                   "mime_type": mimetype,
                                   "afile": str(video.video).split('/')[-1].replace('mp4', 'mp3'),
                                   # "parsed": parsed,
                                   "amimetype": mimetypes.types_map['.mp3'],
                                   "err": recognized['msg'],
                                   "code": recognized['code'],
                                   }
                                  )

                # elif platform['platform'].lower() == 'tiktok.com':
                #     platform_short_name = 'tt'
                #     url = URL()
                #     url.url = link
                #     url.platform_long = platform['platform']
                #     url.platform_short = platform_short_name
                #     url.save()
                #     details = download_video_tiktok(link)
                #     print(details)
                # else:
                #     return render(request, template_name='error.html', context={"title": "Error", 'url': link})

                # return render(request, template_name='error.html', context={"title": "Error", 'err': link})
            elif platform['msg'] == 'fail':
                return render(request, template_name='error.html',
                              context={"title": "Error", 'url': link,
                                       "code": '404', 'err': 'Unsupported platform'})
        else:
            return redirect(to='main')
    else:
        return redirect(to='main')


def test(request):
    return redirect(to='main')
    # return render(request, 'video.html',
    #               {"STATIC_URL": STATIC_URL,
    #                'file': '3NG_aGKJZHg.mkv',
    #                'mime_type': mimetypes.types_map['.mkv']})


def download_file(request, filepath):
    # fill these variables with real values
    print(request)
    fl_path = BASE_DIR / 'static' / 'video' / filepath
    # filename = fl_path.split('/')[-1]
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response


def download_music(request, music):
    details = Music.objects.get(pk=int(music))
    query = "{0} {1}".format(details.artist, details.name)
    results = search_n_download_music(query)
    if results['msg'] == 'success':
        filepath = results['filename']
        fl_path = BASE_DIR / 'static' / 'music' / filepath
        # filename = fl_path.split('/')[-1]
        fl = open(fl_path, 'rb')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filepath
        return response
    # print(request, music, query, results)
    else:
        msg = f'We couldn\'t find the satisfied results from our provider. Try searching the song on <a href="{GOOGLE_QUERY + query}" target="_blank">Google</a>'
        return HttpResponse(msg)


def page404(request, exception):
    data = {"name": "adven.uz"}
    return render(request, "404.html", data)
