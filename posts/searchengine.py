from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document,Keyword,Search,Integer,Text
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models
connections.create_connection(hosts=['localhost'])
#print("hi")

class PostIndex(Document):
    id = Keyword()
    menu_id=Integer()
    article_id=Integer()
    user_id=Keyword()
    title = Text()
    post_content = Text()
    views=Integer()
    post_reg_date=Keyword()
    class Index:
        name = 'brand-search'


def bulk_indexing():
    #PostIndex.init()
    es = Elasticsearch(['localhost'])
    bulk(client=es, actions=(b.indexing() for b in models.PostTab.objects.filter(crawl_flag=1).iterator()))
