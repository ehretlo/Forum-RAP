# Generated by Django 5.0 on 2024-03-05 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppRAP', '0006_alter_post_content_alter_post_hashtags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]
