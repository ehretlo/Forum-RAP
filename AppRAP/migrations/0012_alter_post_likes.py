# Generated by Django 5.0 on 2024-03-06 13:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppRAP', '0011_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='blog_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]