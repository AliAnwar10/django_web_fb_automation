from django.shortcuts import render
from django import forms
from .models import Credential, GroupLink, Post

class CredentialForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded', 'placeholder': 'Enter password'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded', 'placeholder': 'Enter email'
    }))

    class Meta:
        model = Credential
        fields = ['email', 'password']

class GroupLinkForm(forms.ModelForm):
    group_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded', 'placeholder': 'Enter group name'
    }))
    group_url = forms.URLField(widget=forms.URLInput(attrs={
        'class': 'form-control rounded', 'placeholder': 'Enter group URL'
    }))

    class Meta:
        model = GroupLink
        fields = ['group_name', 'group_url']

class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded', 'placeholder': 'Enter post title'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control rounded', 'placeholder': 'Enter post description', 'rows': 4
    }))
    hashtags = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded', 'placeholder': '#hashtag1 #hashtag2', 'required': False
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control rounded'
    }), required=False)

    class Meta:
        model = Post
        fields = ['title', 'description', 'hashtags', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("Only PNG, JPG, or JPEG files are allowed.")
        return image