from django.urls import path
from .views import UsersAPI


user_create = UsersAPI.as_view({
    'get': 'list',
    'post': 'create'
})

app_name = 'users'
urlpatterns = [
    path('', user_create, name='create'),
]