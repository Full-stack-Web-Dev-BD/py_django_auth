from django.db import models
from django.contrib.auth import get_user_model

User= get_user_model()
# Create your models here.
class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    user_id=models.IntegerField()
    bio=models.TextField(blank=True)
    profilepic= models.ImageField(upload_to='profile_pic', default='default.png')
    location=models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.user.username