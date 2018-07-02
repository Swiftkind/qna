from django.db import models
from users.models import User


class Question(models.Model):
    """ Question model
    """
    title = models.CharField(max_length=500)
    content = models.TextField()
    code = models.CharField(max_length=8, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category')
    tags = models.ManyToManyField('Tag')

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    """ Category model
    """
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """ Tag model
    """
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
