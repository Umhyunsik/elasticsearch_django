from django.contrib import admin
from django.urls import path,include
from .views import *
from .models import *
urlpatterns = [
    path("", hello, name='default_page'),
    #아래오는 app name
]