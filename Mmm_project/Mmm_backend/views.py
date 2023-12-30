from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import * 
from django.db import models
from . models import * 
import datetime

from Mmm_backend.models import * 
from datetime import datetime

# 페이지네이션
from django.core.paginator import Paginator
import requests

# api 모듈 
from . use_api import * 
# from . api_key import * 
import base64

from django.shortcuts import get_object_or_404

# forms.py 
# from Mmm_backend.forms import * 
from django.urls import reverse,reverse_lazy


def index(request):
    songs = Song.objects.all()  # 모든 Song 객체를 쿼리
    return render(request, "main/index.html", {'songs': songs})

def Splash(request):
    return render(request,'main/splash.html')


# class MusicList(ListView):
#     model = Song
#     template_name = 'main/list_page.html'
#     context_object_name = "songs"  # 이것을 복수형으로 변경하는 것이 좋습니다.
#     paginate_by = 10

#     def get_queryset(self):
#         # Album과 관련된 Song 객체를 가져오기
#         return Song.objects.select_related('album').all()


# 프로필 
class ProfileView(DetailView):
    model = User 
    template_name = "main/my-info.html"
    pk_url_kwarg = "user_id"
    
    context_object_name = "profile_user"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['liked_songs'] = Liked_Song.objects.filter(user=user).select_related('song')
        
        return context

class UserLikedSongsView(DetailView):
    model = User
    template_name = 'main/my-liked-songs.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['liked_songs'] = Liked_Song.objects.filter(user=user).select_related('song')
        return context
    

# # 프로필 변경 

# class ProfileUpdateView(UpdateView):
#     model = User 
#     form_class = ProfileForm 
#     template_name = "main/profile_update_form.html"
    
#     raise_exception = True # 접근자 제한 
#     redirect_unauthenticated_users = False # 접근자 제한  
    
#     def get_object(self,query=None):
#         return self.request.user 
    
#     def get_success_url(self):
#         return reverse("profile",kwargs=({"user_id":self.request.user.id}))


# # 특정 음악 클릭했을 때 디테일 페이지
# # Song,Album,Artists 모두 연결 
# class MusicDetailView(DetailView):
#     model = Song
#     template_name = "main/detail_page.html"
#     pk_url_kwarg = 'song_id'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         song = self.object  # 현재 곡 객체
#         context['album'] = song.album  # 연결된 앨범
#         context['artist'] = song.album.artist  # 연결된 아티스트
#         return context

# # 앨범 디테일 페이지 

# class AlbumDetailView(DetailView):
#     model = Album
#     template_name = "main/album_detail_page.html"
#     pk_url_kwarg = 'album_id'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         album = self.object  # 현재 앨범 객체
#         context['songs'] = Song.objects.filter(album=album)  # 현재 앨범과 연결된 곡들
#         context['artist'] = album.artist  # 현재 앨범과 연결된 아티스트
#         return context

# class ArtistDetailView(DetailView):
#     model = Artist
#     template_name = "main/artist_detail_page.html"
#     pk_url_kwarg = "artist_id"
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         artist_id = self.kwargs.get('artist_id')
#         # Song 모델에서 아티스트를 찾을 때 album을 통해 접근
#         context['songs'] = Song.objects.filter(album__artist__id=artist_id)
#         return context

# def search_track(request):
#     context = {}
#     if request.method == "POST":
#         track_name = request.POST.get('query')
#         api = UseApi(client_id_spotify, client_pw_spotify)  # Spotify API 인스턴스 생성
#         tracks = api.search_track([track_name])
#         album_data = []
#         artist_data = []
#         song_data = []
#         feature_data = []
#         for track in tracks:
#             album = api.get_track_details(track["track_id"])[0]
#             artist = api.get_track_details(track["track_id"])[1]
#             song = api.get_track_details(track["track_id"])[2]
#             feature = api.get_track_details(track["track_id"])[3]
#             album_data.append(album)
#             artist_data.append(artist)
#             song_data.append(song)
#             feature_data.append(feature)
#         paginator = Paginator(album_songs, 10)  # 여기서 10은 한 페이지에 표시할 항목 수
#         page_number = request.GET.get('page')
#         album_songs = Song.objects.filter(album=album).order_by('title')
#         page_obj = paginator.get_page(page_number)
#         # 검색 결과를 context에 추가
#         context= {
#             'artist': artist_data,
#             'album': album_data,
#             'song': song_data,
#             'album_songs': page_obj,
#             'features': feature_data
#         }
#     # 검색 결과와 함께 템플릿 렌더링
#     return render(request, 'main/search_result.html', context)