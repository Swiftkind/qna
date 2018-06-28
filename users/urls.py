from django.urls import path, include
from .views import UserRegistrationAPI, UserAPI


user_create = UserRegistrationAPI.as_view({
    'get': 'list',
    'post': 'create'
})

user_login =  UserRegistrationAPI.as_view({
        'post':'login',
        'get':'list',
    })

user_get_hash = UserAPI.as_view({
    'get': 'get_hash'
})

user_changepass = UserAPI.as_view({
    'post': 'changepass'
})

app_name = 'users'
urlpatterns = [
    path('create/', user_create, name='create'),
    path('login/',user_login, name='user_login'),
    path('gethash/',user_get_hash, name='get_hash'),
    path('reset/<str:hash>',user_changepass, name='changepass'),
]
