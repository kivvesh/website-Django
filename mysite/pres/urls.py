from django.urls import path
from .views import *

urlpatterns = [
    #path('',index, name ='home'),
    path('',HomePres.as_view(), name ='home'),
    #path('category/<int:category_id>/',get_category,name = 'category'),
    path('category/<int:category_id>/',PresByCategory.as_view(),name = 'category'),
    #path('pres/<int:pres_id>',view_pres,name='view_pres'),
    path('pres/<int:pk>/', ViewPres.as_view(), name='view_pres'),
    #path('pres/add-pres',add_pres,name = 'add_pres'),
    path('pres/add-pres',CreatePres.as_view(),name = 'add_pres'),
    path('register/',register,name='register'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('email/',email,name='email')
]