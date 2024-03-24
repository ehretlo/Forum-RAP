from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django import forms
from AppRAP.models import Post

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    class Meta:
        model = get_user_model()  # Obtient le modèle utilisateur actuel
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)  # Appelle la méthode save() du formulaire parent
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.password = make_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'hashtags', 'mentions']

# REGISTRER NON FONCTIONNEL
def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé avec succès. Veuillez vous connecter.")
            return redirect("login_user")
    else:
        form = SignupForm()

    return render(request, "AppRAP/register.html", {"form": form})

    from django import forms

# FORMULAIRE POUR EDITER EN BASE LA DESCRIPTION DE SOI MEME
class EditDescriptionForm(forms.Form):
    description = forms.CharField(label='Nouvelle description', widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))

# MODIFIER LABEL POUR METTRE UN TITRE
class PostSearchForm(forms.Form):
    query = forms.CharField(label='', max_length=100)