# Generated by Django 3.1.7 on 2021-04-12 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0008_auto_20210413_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='投稿画像'),
        ),
        migrations.AddField(
            model_name='topic',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='投稿画像'),
        ),
    ]