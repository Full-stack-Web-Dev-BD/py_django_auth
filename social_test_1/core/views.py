from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/signin')
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            # check if user exist already
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email is already registered")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "username is already token")
                return redirect('signup')
            else:
                # Register user
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                # login user and redirect to settings page
                # create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Both password not matched')
            return redirect('signup')

    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        print(username, password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Incorrect username or password")
            return redirect('signin')
    else:
        return render(request, 'signin.html')


@login_required(login_url='/signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

