from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Mmm_backend.urls')),
    
    # all-auth
    path('accounts/',include('allauth.urls')),
]
