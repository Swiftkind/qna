from django.urls import path
from .views import QuestionAPI


question_list = QuestionAPI.as_view({
    'get': 'list',
    'post': 'create',
})

question_search = QuestionAPI.as_view({
    'get': 'list',
    'post': 'search',
})

question_details = QuestionAPI.as_view({
    'get':'details',
    'post':'edit',
})

app_name = 'api'
urlpatterns = [
    path('', question_list, name='list'),
    path('search/', question_search, name='search'),
    path('<str:code>/', question_details, name='details'),
]
