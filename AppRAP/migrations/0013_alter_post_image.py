# Generated by Django 5.0 on 2024-03-06 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppRAP', '0012_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]
