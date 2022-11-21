from django.contrib import admin
from .models import Pres, Category

class PresAdmin(admin.ModelAdmin):
    list_display = ('id','category','title','created_at','update_at','is_published')
    list_display_links = ['id','title']
    search_fields = ['title','content']
    list_editable = ('is_published',)
    list_filter = ('is_published','category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ['id','title']
    search_fields = ['title']

admin.site.register(Pres,PresAdmin)

admin.site.register(Category,CategoryAdmin)

