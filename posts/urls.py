from django.urls import path
from .views import *
from .models import *


app_name='posts'


urlpatterns=[
   path('',searchresult,name='query_list'),
]