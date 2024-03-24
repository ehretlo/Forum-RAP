from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from requests import post
from AppRAP.models import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import *
from .models import Post
from .models import User
from .forms import LoginForm
from .forms import EditDescriptionForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from .models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserChangeForm
from .forms import EditDescriptionForm
from .models import Post, Comment

# PAGE HOME 
def home(request):
    if request.user.is_authenticated:    
        followed_users = request.user.follows.all()

        posts = Post.objects.filter(creator__in=followed_users)


        context = { 'posts': posts,  } 
        return render(request, 'AppRAP/home.html', context)
    else:
        return render(request, 'AppRAP/no_authenticated.html')

# PAGE DECOUVERTE
def decouverte(request):
    if request.user.is_authenticated: 
        posts = Post.objects.all()
        context = { 'posts': posts, } 
        return render(request, 'AppRAP/decouverte.html' , context)
    else:
        return render(request, 'AppRAP/no_authenticated.html')
    
# AUTH USER A GARDER
def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("../home/")
        else:
            messages.info(request, "Identifiant ou mot de passe incorrect")

    return render(request, "AppRAP/login.html", {"form": form})
    
# DECONNEXION USER
def logout_user(request):
    logout(request)
    return redirect("../login/")

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connectez automatiquement l'utilisateur après l'inscription
            return redirect('home')  # Redirigez l'utilisateur vers la page d'accueil après l'inscription
    else:
        form = SignupForm()
    return render(request, 'AppRAP/register.html', {'form': form})

# VUE OUR LE PROFIL PERSONNEL A SOI (modifs et mise à jour de ses infos)
def profile_view(request):
    if request.user.is_authenticated: 
        followed_users = request.user.follows.all()
        me = request.user
        followers = get_user_model().objects.filter(follows=me)
        user_posts = Post.objects.filter(creator=me)
        context = { 'followed_users': followed_users, 
                    'user_posts': user_posts,
                    'followers' : followers,
                    'Nom ' : me.last_name,
                    'Prénom' : me.first_name,
                    'Email': me.email,

                    } 
        return render(request, 'AppRAP/profile.html', context)
    else:
        return render(request, 'AppRAP/no_authenticated.html')

def redirect_to_login(request):
    return redirect('login')


def message_view(request):
    if request.user.is_authenticated: 

        chats = Chat.objects.filter(participants=request.user)

        context = { 'chats': chats,  } 
        return render(request, 'AppRAP/message.html', context)
    else:
        return render(request, 'AppRAP/no_authenticated.html')
    
def conv_view(request, chat_id):
    conv = get_object_or_404(Chat, pk=chat_id)
    messages = conv.messages.all()
    context = {'conv': conv, 'messages': messages}
    return render(request, 'AppRAP/conv.html', context)

# VUE POUR LA CREATION D'ARTICLE ET REDIRECTION VERS create_article.html
def create_article(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Prenez en charge les fichiers envoyés
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user  # Assigner l'utilisateur actuel comme créateur du post
            post.save()
            return redirect('/home/')  # Rediriger vers la page d'accueil
    else:
        form = PostForm()
    return render(request, 'AppRAP/create_article.html', {'form': form})

# VUE POUR LES UTILISATEURS QUI VISITENT UN COMPTE (path   path('profil/<str:username>/', views.user_profile, name='user_profile'),)
@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = user.post_set.all()
    followers = user.follows.all()
    return render(request, 'AppRAP/user_profile.html', {'user': user, 'user_posts': user_posts, 'followers': followers})

# BOUTON FOLLOW
@login_required
def toggle_follow(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)
    user = request.user
    if user in profile.follows.all():
        profile.follows.remove(user)
    else:
        profile.follows.add(user)
    return redirect('AppRAP/user_profile.html', username=username)


# VUE POUR SE DECONNECTER
def logout_view(request):
    logout(request)
    return render(request, 'users/index.html')

# VUE POUR EDITER LA DESCRIPTION (en lien avec EditDescriptionForm dans forms.py )
def edit_description_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    form = EditDescriptionForm(request.POST or None, initial={'description': request.user.description})
    if request.method == 'POST':
        if form.is_valid():
            new_description = form.cleaned_data['description']
            request.user.description = new_description
            request.user.save()
            return redirect('/profil/')
    context = {'form': form}
    return render(request, "AppRAP/edit_description.html", context)

#VUE POUR LA RECHERCHE DE PUBLICATIONS AVEC L'UTILITAIRE PAGINATOR 
def post_search(request):
    form = PostSearchForm(request.GET)
    query = request.GET.get('query', '')

    if query:
        posts = Post.objects.filter(content__icontains=query)
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'AppRAP/recherche.html', {'form': form, 'posts': page_obj})

# VUE POUR SUPPRIMER UN POSTE EN BASE AVEC LE RACCOURCI 404 DE DJANGO (SI ERREUR IL Y A), redirect vers decouverte (car bouton sur decouverte)
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.creator:
        post.delete()
    return redirect('decouverte')

# VUE DU BOUTON S'ABONNER (DECLENCHE DE BASE) OU QUAND LE BOUTON SE DESABONNER EST APPUYE
@login_required
def subscribe_view(request, user_id):
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, id=user_id)
        request.user.follows.add(user_to_follow)
        return redirect('user_profile', username=user_to_follow.username) 
    else:
        return redirect('decouverte')

# VUE DU BOUTON SE DESABONNER OU QUAND LE BOUTON S'ABONNER EST APPUYE
@login_required
def unsubscribe_user(request, username):
    if request.method == 'POST':
        user_to_unfollow = get_object_or_404(User, username=username)
        request.user.follows.remove(user_to_unfollow)
        return redirect('user_profile', username=username)
    else:
        return redirect('decouverte')

#MODIFIER SON USERNAME POUR TOUT LE MONDE
@login_required
def edit_username_view(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        if User.objects.filter(username=new_username).exists():
            messages.error(request, "Déjà utilisé !")
            return redirect('profile_view')
        user = request.user
        user.username = new_username
        user.save()
        messages.success(request, "Votre nom d'utilisateur a été modifié avec succès.")
        return redirect('profile_view')
    else:
        return render(request, 'AppRAP/edit_username.html')

# DETAIL EN GRAND DU POSTE
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'AppRAP/post_detail.html', {'post': post, 'comments': comments})