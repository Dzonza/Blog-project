from django import forms 
from .models import Post, Comment, UserProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
        labels = {
            'image' : 'Profile Picture',
        }

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        label = {
            'text': 'Text',
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = [ 'author', 'slug',]
        labels = { 
            'title': 'Title',
            'content': 'Content',
            'excerpt': 'Excerpt',
            'image': 'image',
            'tags': 'Tags',
        }

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'date', 'slug']
        labels = {
            'title': 'Title',
            'excerpt': 'Excerpt',
            'content': 'Content',
            'image': 'Image',
            'tags': 'Tags',
        }

class EditProfile(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields= ('username', 'first_name', 'last_name', 'email')
        labels= {
            'username' : 'Username',
            'first_name' : 'First Name',
            'last_name' : 'Last Name',
            'email' : 'Email',
        }