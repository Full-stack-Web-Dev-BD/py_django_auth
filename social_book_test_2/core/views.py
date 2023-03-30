from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    print(request.user.is_authenticated)
    if  request.user.is_authenticated :
        return render(request,'index.html')
    else:
        messages.info(request, "You are not authenticated")
        return redirect('login')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            # look for if user exist
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already in use")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already in use")
                return redirect("register")
            else:
                # create new user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # create  Profile
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                # sign in user and redirect to priflle page 
                auth.login(request, user_model)
                messages.info(request, "Logged in & User profile created successfully")
                return redirect('profile')
        else:
            messages.info(request, "Both password and password2 are different")
            return redirect('register')
    else:
        return render(request,'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        if User.objects.filter(username=username).exists()== False :
            messages.info(request, "User not Found: %s" % username)
            return  redirect('login')
        elif authenticate(username=username, password=password) is not None :
            user= User.objects.get(username=username)
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('login')
    return render(request, 'login.html')

@login_required(login_url="login")
def logout(request):
    auth.logout(request) 
    messages.info(request,"Logged out successfully")
    return redirect('login')

@login_required(login_url="login")
def profile(request):
    if request.user.is_authenticated is not None:
        return render(request, 'profile.html')
    else:
        messages.info(request, "You are not authenticated")
        return redirect('login') 
