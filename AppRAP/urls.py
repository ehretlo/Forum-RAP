from django.urls import path
from . import views
from .views import profile_view
from django.contrib.auth import views as auth_views
from .views import edit_description_view
from .views import user_profile, edit_description_view


urlpatterns = [
    path("", views.redirect_to_login),
    path("home/", views.home, name='home'),
    path("decouverte/", views.decouverte, name='decouverte'),
    path("login/", views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path("profil/", views.profile_view, name='profile_view'),
    path("message/", views.message_view, name='message_view' ),
    path('create/', views.create_article, name='create_article'),
    path('message/<int:chat_id>/', views.conv_view, name='conv_view'),
    path('profil/<str:username>/', views.user_profile, name='user_profile'),
    path('edit_description/', edit_description_view, name='edit_description'),
    path('post/search/', views.post_search, name='post_search'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('subscribe_user/<int:user_id>/', views.subscribe_view, name='subscribe_user'),
    path('unsubscribe_user/<str:username>/', views.unsubscribe_user, name='unsubscribe_user'),
    path('toggle_follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('modify_username/', views.edit_username_view, name='modify_username'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]