from django.urls import path
from .views import QuestionAPI


question_list = QuestionAPI.as_view({
    'get': 'list',
    'post': 'create',
})

question_details = QuestionAPI.as_view({
    'get':'details',
    'post':'edit',
})

app_name = 'questions'
urlpatterns = [
    path('', question_list, name='list'),
    path('<str:code>/', question_details, name='details'),
]
