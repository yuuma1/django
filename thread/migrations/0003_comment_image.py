# Generated by Django 3.1.7 on 2021-04-05 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0002_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='投稿画像'),
        ),
    ]