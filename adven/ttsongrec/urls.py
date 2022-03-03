from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from adven.ttsongrec.models import Music


# Serializers define the API representation.
class MusicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Music
        fields = ['pk', 'name', 'link', 'file', 'artist', 'album', 'filesize']


# ViewSets define the view behavior.
class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'music', MusicViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('getmusic/', include('rest_framework.urls', namespace='rest_framework'))
]
# urlpatterns = [
#     path('', recognizer, name='recognizer')
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
