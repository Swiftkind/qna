from django.urls import path, include
from .views import UserAuthView, UsersAPI

user_create = UsersAPI.as_view({
    'get': 'list',
    'post': 'create'
    })

user_login =  UserAuthView.as_view({
        'post':'login',
        'get':'user_list',
    })

app_name = 'users'
urlpatterns = [
    path('login/',user_login, name='user_login'),
    path('', user_create, name='create'),
]