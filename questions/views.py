from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import QuestionSerializer
from .models import Question


class QuestionAPI(ViewSet):
    """ Questions API
    """
    permission_classes = (IsAuthenticated,)

    def list(self, *args, **kwargs):
        """ lists all questions
        """
        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True)
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
