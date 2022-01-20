from django.shortcuts import render

from .forms import LinkForm
from .models import URL, Video, Music, Recognized

# Create your views here.
from .utils import extract_platform, download_video_shorts, download_video_tiktok


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
                if platform['platform'].lower() == 'youtube.com':
                    platform_short_name = 'yt'
                    url = URL()
                    url.url = link
                    url.platform_long = platform['platform']
                    url.platform_short = platform_short_name
                    url.save()
                    details = download_video_shorts(link)
                    print(details)
                    video = Video()
                    video.video_id = details['video_id']
                    video.url = url
                    video.title = details['title']
                    video.thumb = details['thumb']
                    video.description = details['description']
                    video.video = details['full_path']

                elif platform['platform'].lower() == 'tiktok.com':
                    platform_short_name = 'tt'
                    url = URL()
                    url.url = link
                    url.platform_long = platform['platform']
                    url.platform_short = platform_short_name
                    url.save()
                    details = download_video_tiktok(link)
                else:
                    return render(request, template_name='error.html', context={"title": "Error", 'url': link})

                return render(request, template_name='detected.html', context={"title": "Form", 'link': link})
            elif platform['msg'] == 'fail':
                return render(request, template_name='error.html', context={"title": "Error", 'url': link})

    else:
        form = LinkForm()
        print(3, form)
    return render(request, 'detected.html', {'form': form, 'title': 'Form'})
