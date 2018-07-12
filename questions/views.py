from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .serializers import QuestionSerializer
from .models import Question


class QuestionAPI(GenericViewSet, ListModelMixin):
    """ Questions API
    """
    # permission_classes = (IsAuthenticated,)

    def list(self, *args, **kwargs):
        """ lists all questions
        """
        questions = Question.objects.all()

        page = self.request.GET['page']
        try:
            page = self.paginate_queryset(questions)
        except:
            return Response(status=404)

        serializer = QuestionSerializer(page, many=True)
        return Response(serializer.data, status=200)

    def create(self, *args, **kwargs):
        """ creates a question
        """
        serializer = QuestionSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save(self.request.user)
            return Response(status=201)
        return Response(serializer.errors, status=400)

    def details(self, *args, **kwargs):
        """ view details of a question
        """
        code = self.kwargs.get('code', None)
        question = Question.objects.get(code=code)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=200)

    def edit(self, *args, **kwargs):
        """ edit details of an existing question
        """
        code = self.kwargs.get('code', None)
        question = Question.objects.get(code=code)
        if question.user == self.request.user:
            serializer = QuestionSerializer(data=self.request.data)
            if serializer.is_valid():
                serializer.update(question.id)
                return Response(status=201)
        return Response(status=400)

    def search(self, *args, **kwargs):
        """ lists searched questions
        """
        keyword = self.request.POST['keyword']
        questions = Question.objects.filter(
                            Q(title__icontains=keyword)|
                            Q(content__icontains=keyword)|
                            Q(categories__name__icontains=keyword)|
                            Q(tags__name__icontains=keyword)).distinct()

        page = self.request.GET['page']
        try:
            page = self.paginate_queryset(questions)
        except:
            return Response(status=404)

        serializer = QuestionSerializer(page, many=True)
        return Response(serializer.data, status=200)
