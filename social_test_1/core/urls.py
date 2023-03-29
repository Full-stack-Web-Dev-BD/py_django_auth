from django.urls import path
from . import views


# Set URLS  
urlpatterns=[
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('logout', views.logout, name="logout"),
]