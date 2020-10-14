from django.shortcuts import render,get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.db import connection
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elasticsearch import Elasticsearch
from rest_framework.decorators import api_view, renderer_classes
from django.utils.safestring import mark_safe
import json
import math
from django.views.decorators.http import require_http_methods,require_GET
from django.http import HttpResponseRedirect


class temp:
    def __init__(self, title, user_id, views, post_reg_date, post_content):
        self.title = title
        self.user_id = user_id
        self.views = views
        self.post_reg_date = post_reg_date
        self.post_content = post_content


def show_post_list(request):
    # 보여줄 사진 데이터
    post_list=PostTab.objects.filter(crawl_flag=1)

    paginator = Paginator(post_list, 20)
    page = int(request.GET.get('p',1))
    post_list = paginator.get_page(page)

    return render(request,'posts/searchposts.html',{'posts':post_list})
    # render는 화면에표시 하는것
    # template폴더에서부터 user 밑에 list라는 것임
    # 템플릿안에서는 food_store 라는 이름으로 쓰겠다. but object_list가 기본임 !

#@require_GET
def searchresult(request,*args,**kwargs):
   # print("들어옴")
    search_all=False
    if 'drop' in request.GET:
        if (request.GET['drop'])=='1':
            search_all=True
            #print("enter drop")

    object_list = []
    es = Elasticsearch()
    return_list=[]
    if 'q' in request.GET:
        query = request.GET.get('q')
       # print(query)
        if not query:
            #print("enter")
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'search word param is missing'})
        if search_all:
            docs=es.search(
                index='brand-search',
                body={
                   "size":60,
                       "query": {
                         "multi_match": {
                           "query": query,
                           "fields":["title","post_content"]
                         }
                       },
                          "highlight": {
                            "pre_tags": ["<mark><strong>"],
                            "post_tags": ["</strong></mark>"],
                            "fields": {
                            "post_content": {},

                            }
                          },
                     })
            print("enter")

        else:
            #print(request.GET['drop'])
            docs = es.search(index='brand-search',
                             body={
                                 "size": 60,

                                     "query": {
                                         "bool": {
                                             "must": {
                                                 "multi_match": {
                                                     "query": query,
                                                     "fields": [
                                                         "post_content",
                                                         "title"
                                                     ]
                                                 }
                                             },
                                             "filter": {
                                                 "term": {
                                                     "menu_id": request.GET['drop']
                                                 }
                                             }

                                         }
                                     },
                                 "highlight": {
                                     "pre_tags": ["<mark><strong>"],
                                     "post_tags": ["</strong></mark>"],
                                     "fields": {
                                         "post_content": {},

                                     }
                                     }
                                     })

        data_list = docs['hits']
       # print(data_list)
        return_list=[]
        object_list=[]
        for i in  data_list['hits']:
            title=i['_source']['title']
            user_id=i['_source']['user_id']
            views=i['_source']['views']
            post_reg_date=i['_source']['post_reg_date'].replace(":00+00:00","").replace("T"," ")
            try:
                post_content=mark_safe(i['highlight']['post_content'][0])

            except:
                post_content = (i['_source']['post_content'])
           # print(post_content)

            object_list.append(temp(title,user_id,views,post_reg_date,post_content))
            return_list.append([title,user_id,views,post_reg_date,post_content])
        paginator = Paginator(object_list, 20)
        page = int(request.GET.get('p', 1))
        object_list = paginator.get_page(page)

    return render(request,'posts/searchresults.html',{'docs':object_list,'lendocs':len(return_list)})
