from django.urls import path, include
from .views import UserAuthView

app_name = 'users'
urlpatterns = [
    path('login/', UserAuthView.as_view({
        'post':'login',
        'get':'user_list',
    }), name='user_login'),
]