from django.urls import path,include
from .views import *

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='logout'),
    path('user_registration/', user_registration, name='user_registration'),
    path('user_list/', user_list, name='user_list'),
    path('signup/', signup_views, name='signup'),

]