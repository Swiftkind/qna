# Generated by Django 2.0.6 on 2018-06-28 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_confirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmation',
            name='url',
            field=models.CharField(default='', max_length=500),
        ),
    ]
