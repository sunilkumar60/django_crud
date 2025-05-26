from django.db import models

# Create your models here.

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20, null=True, blank=True)

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details', null=True)
    profile_picture = models.FileField(upload_to="profile_picture/", null=True, blank=True)
    country = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)