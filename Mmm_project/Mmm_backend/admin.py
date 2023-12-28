from django.contrib import admin
from .models import * 
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(User,UserAdmin)

UserAdmin.fieldsets += (('Custom fields',{'fields':('nickname','profile_pic','intro')}),)