from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import fields

# from .models import User

class LoginForm(AuthenticationForm):

    class Meta:
        model = get_user_model()
        fields = ['username','password']

    def __init__(self, *args, **kwargs ):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['auto-focus'] = True
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

class CustomUserCreation(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = ['username','first_name', 'last_name', 'is_manager']
    
    def __init__(self, *args, **kwargs ):
        super(CustomUserCreation, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['is_manager'].widget.attrs['class'] = 'form-check-input'


class DisableUser(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['is_active']

    def __init__(self, *args, **kwargs):
        super(DisableUser, self).__init__(*args, **kwargs)
        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'