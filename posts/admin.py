from django.contrib import admin
from .models import *


# Register your models here.
class RestseedtabAdmin(admin.ModelAdmin):
    list_display = ['id','menu_id','title','post_content']
    list_filter = ['menu_id','title']
admin.site.register(PostTab,RestseedtabAdmin)

