from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
from ProjetRAP import settings
from django.contrib.auth import get_user_model




class User(AbstractUser):
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True, help_text="Format: YYYY-MM-DD")
    country = models.ForeignKey("Country", on_delete=models.SET_NULL, null=True)
    follows = models.ManyToManyField("self", related_name="followed_by",symmetrical=False,blank=True)
    #blockers = models.ManyToManyField("self")
    

    class Meta:
        db_table = "auth_user"

    def __str__(self) -> str:
        return f"{self.username}"
    

    def birth_valid(self) -> bool:
        min_old = timezone.now() - datetime.timedelta(days=5840)
        max_old = timezone.now() - datetime.timedelta(days=36500)
        return self.birth_date <= min_old and self.birth_date >= max_old
    
    # def block_is_True(self, other) -> bool:
    #     return self.blockers.contains(other)
    
    # def follow_is_True(self, other) -> bool:
    #     return self.followers.contains(other)

class Post(models.Model):
    creator = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=700,blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField('Hashtag',blank=True)
    mentions = models.ManyToManyField('Mention',blank=True)
    likes = models.ManyToManyField(User, related_name='blog_posts',blank=True)


    def __str__(self):
        return f"Post by {self.creator.username}"


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    name = models.CharField(max_length=30)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING , default=None)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages' , default=None)
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message {self.content} "

class Country(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return f"Country: {self.name}"

    
class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Mention(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=None)
    

    def __str__(self):
        return f"Mention of {self.user.username}"


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"