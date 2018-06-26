from django.urls import path, include
from .views import UserAuthView

app_name = 'users'
urlpatterns = [
    path('login/', UserAuthView.as_view(), name='user_login'),
]