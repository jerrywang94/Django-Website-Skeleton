from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import UserInfo

#-------------------------------------------------------------------------------
#   Simple widget to force radio buttons to be aligned horizontally
class HorizontalRadioSelect(forms.RadioSelect):
    template_name = 'horizontal_select.html'

#-------------------------------------------------------------------------------
#   Registration form for User Creation
#   Required fields for user are: first name, last name, email
#   Email is used as username
class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=True, help_text='')
    last_name = forms.CharField(max_length=30, required=True, help_text='')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid E-mail address. This will be your username.')

    class Meta:
        model = UserInfo
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )

    def save(self, *args, **kwargs):
        user = super(SignUpForm, self).save(commit=False, *args, **kwargs)
        # Force username to be user email
        user.username = self.cleaned_data['email']
        user.save()
        return user

#-----------------------------------------
#   Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        # If authenticate fails, user will not be set
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
