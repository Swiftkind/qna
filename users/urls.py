from django.urls import path
from .views import GuestAPI, UserAPI


user_create = GuestAPI.as_view({
    'get': 'list',
    'post': 'create'
})

user_login =  GuestAPI.as_view({
    'post':'login',
    'get':'list',
})

user_details = UserAPI.as_view({
    'get':'details',
    'post':'edit',
})

user_get_hash = GuestAPI.as_view({
    'post': 'get_hash'
})

user_changepass = UserAPI.as_view({
    'get': 'check_valid',
    'post': 'changepass'
})

app_name = 'users'
urlpatterns = [
    path('create/', user_create, name='create'),
    path('login/', user_login, name='login'),
    path('gethash/', user_get_hash, name='get_hash'),
    path('reset/<str:hash>/', user_changepass, name='changepass'),
    path('<str:handle>/', user_details, name='details'),
]
