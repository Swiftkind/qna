from rest_framework import serializers
from .models import Question
import uuid


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer of a question"""
    user = serializers.EmailField(read_only=True)
    code = serializers.CharField(read_only=True)

    class Meta:
        model = Question
        fields = ('__all__')

    def save(self, user):
        question = Question.objects.create(title=self.validated_data['title'],
                                    content=self.validated_data['content'],
                                    code=self.generate_code(),
                                    user=user)
        for category in self.validated_data['categories']:
            question.categories.add(category)
        for tag in self.validated_data['tags']:
            question.tags.add(tag)
        question.save()
        
    def generate_code(self):
        code = f"{uuid.uuid4().hex[:8]}"
        try:
            question = Question.objects.get(code=code)
        except Question.DoesNotExist:
            return code
        else:
            return generate_code()

    def update(self, id):
        question = Question.objects.get(id=id)
        question.title = self.validated_data['title']
        question.content = self.validated_data['content']

        question.categories.set(self.validated_data['categories'])
        question.tags.set(self.validated_data['tags'])

        question.save()
