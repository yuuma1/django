# Generated by Django 3.1.7 on 2021-04-12 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0007_topic_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='image',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='image',
        ),
    ]
