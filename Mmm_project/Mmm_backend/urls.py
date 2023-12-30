from django.urls import path
from . import views
from .models import * 

urlpatterns = [
    path('',views.Splash, name='splash'),
    path('index/',views.index,name="index"),

    path('users/<int:user_id>/',views.ProfileView.as_view(),name="profile"),
    path('users/<int:pk>/liked-songs/',views.UserLikedSongsView.as_view(), name='user_liked_songs'),
]