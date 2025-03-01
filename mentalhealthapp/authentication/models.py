from django.db import models

class UserProfile(models.Model):
    uid = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20)
