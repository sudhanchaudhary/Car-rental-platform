from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    profilepic=models.ImageField(upload_to='profile',null=True,blank=True)
    fname=models.CharField(max_length=200)
    lname=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)
    address=models.CharField(max_length=300)
    gender=models.CharField(max_length=20)
    citizen=models.CharField(max_length=30)
    citizenfront=models.ImageField(upload_to='Id',null=True,blank=True)
    citizenback=models.ImageField(upload_to='Id',null=True,blank=True)
    licence=models.CharField(max_length=30,null=True,blank=True)
    licencefront=models.ImageField(upload_to='Id',null=True,blank=True)
    licenceback=models.ImageField(upload_to='Id',null=True,blank=True)
    approved=models.BooleanField(default=False)
    account_type=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    