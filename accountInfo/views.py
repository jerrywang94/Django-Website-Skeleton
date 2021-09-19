from django.contrib.auth import login as auth_login, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from .models import UserInfo
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

#-------------------------------------------------------------------------------
#   View for registration page
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Server will check database if same email has already registered
            email = form.cleaned_data.get('email')
            dup_emails = UserInfo.objects.filter(email__icontains=email)
            if dup_emails.exists():
                msg = "Email already registered, please choose another."
                form.add_error("email", u"%s" % msg)
                return render(request, 'accountInfo/register.html', {'form': form})
            else:
                form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accountInfo/register.html', {'form': form})


#-------------------------------------------------------------------------------
#   View for login
def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.login(request)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
    return render(request, 'accountInfo/login.html', {'form': form})

#-------------------------------------------------------------------------------
#   View for password change
def pass_change(request):
    form = PasswordChangeForm(user = request.user, data = request.POST or None)
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('pass_change')
        else:
            messages.error(request, 'Please see errors below.')
    return render(request, 'accountInfo/pass_change.html', { 'form' : form })