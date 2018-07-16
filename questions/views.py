from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from .serializers import QuestionSerializer
from .models import Question


class QuestionAPI(GenericViewSet, ListModelMixin):
    """ Questions API
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()   
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        overrides default queryset
        """
        keyword = self.request.GET.get('keyword', '')
        sortby = self.request.GET.get('sort', 'id')

        questions = Question.objects.filter(
                            Q(title__icontains=keyword)|
                            Q(content__icontains=keyword)|
                            Q(categories__name__icontains=keyword)|
                            Q(tags__name__icontains=keyword)
                            ).order_by(sortby).distinct()

        return questions

    def list(self, request, *args, **kwargs):
        """
        lists questions
        """

        return super(QuestionAPI, self).list(request, *args, **kwargs)

    def create(self, *args, **kwargs):
        """ creates a question
        """
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save(self.request.user)
            return Response(status=201)
        return Response(serializer.errors, status=400)

    def details(self, *args, **kwargs):
        """ view details of a question
        """
        code = self.kwargs.get('code', None)
        question = Question.objects.get(code=code)
        serializer = self.serializer_class(question)
        return Response(serializer.data, status=200)

    def edit(self, *args, **kwargs):
        """ edit details of an existing question
        """
        code = self.kwargs.get('code', None)
        question = Question.objects.get(code=code)
        if question.user == self.request.user:
            serializer = self.serializer_class(data=self.request.data)
            if serializer.is_valid():
                serializer.update(question.id)
                return Response(status=200)
        return Response(status=400)
