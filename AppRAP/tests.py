from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.test import Client
from .models import Post, Chat
from AppRAP.models import *

class BirthdayTest(TestCase):

    # Test date de naissance
    def test_birthday_too_young(self): #16 à 100
        young = timezone.now() - datetime.timedelta(days=5000)
        birth= User(birth_date=young)
        self.assertFalse(birth.birth_valid())


    def test_birthday_too_old(self): #16 à 100
        old = timezone.now() - datetime.timedelta(days=36600)
        birth= User(birth_date=old)
        self.assertFalse(birth.birth_valid())

    def test_birthday_equal_min(self):
        min_old = timezone.now() - datetime.timedelta(days=5840)
        birth= User(birth_date=min_old)
        self.assertTrue(birth.birth_valid())




# Test user bloqué
        
class BlockTest(TestCase):

    def test_blocked_user(self):
        user1 = User.objects.create_user(username='user1', password='test')
        
        user2 = User.objects.create_user(username='user2', password='test')
        userprofil1 = User(user=user1,id=user1)
        userprofil2 = User(user=user2,)
        userprofil1.blockers.add(user2)
        

        
        self.assertTrue(user1.block_is_True(user2))
        self.assertFalse(user2.block_is_True(user1))

        
# Test followers (pareille que block)


class Follow_Test(TestCase):

    def test_following_user(self):
        user3 = User(username='user3', password='test')
        user4 = User(username='user4', password='test')

        user3.followers.add(user4)
        self.assertTrue(user3.follow_is_True(user4))
        self.assertFalse(user4.follow_is_True(user3))

#TESTS DES VUES DE CHAQUE PAGE
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppRAP/home.html')

    def test_decouverte_view(self):
        response = self.client.get(reverse('decouverte'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppRAP/decouverte.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppRAP/login.html')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppRAP/register.html')

    def test_profile_view(self):
        response = self.client.get(reverse('profile_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppRAP/profile.html')

    def test_message_view(self):
        response = self.client.get(reverse('message_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppRAP/message.html')

    def test_create_article_view(self):
        response = self.client.get(reverse('create_article'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppRAP/create_article.html')

    def test_conv_view(self):
        chat = Chat.objects.create()
        response = self.client.get(reverse('conv_view', kwargs={'chat_id': chat.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppRAP/conv.html')
        

#TEST POUR LA CREATION DE POST PAR SOI MEME
class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_post_creation(self):
        post = Post.objects.create(content="Test content", creator=self.user)
        self.assertEqual(post.content, "Test content")
        self.assertEqual(post.creator, self.user)

class EditUsernameViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

def test_edit_username_view_GET(self):
    url = reverse('edit_username')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)