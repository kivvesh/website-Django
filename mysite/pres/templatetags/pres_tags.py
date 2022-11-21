from django import template
from pres.models import Category
from django.db.models import *

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('pres/list_categories.html')
def show_categories():
    categories = Category.objects.filter(get_pres__is_published=True).annotate(cnt=Count('get_pres')).filter(cnt__gt=0)
    return {'categories':categories}
