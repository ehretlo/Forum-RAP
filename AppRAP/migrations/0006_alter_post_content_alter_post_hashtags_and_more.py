# Generated by Django 5.0 on 2024-03-05 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppRAP', '0005_user_follows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='post',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='AppRAP.hashtag'),
        ),
        migrations.AlterField(
            model_name='post',
            name='mentions',
            field=models.ManyToManyField(blank=True, to='AppRAP.mention'),
        ),
    ]