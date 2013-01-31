from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfileManager(models.Model):
    def create_user(self,username,email,password):
        User.objects.create(username,email,password)


class UserProfile(models.Model):
    objects=UserProfileManager()
    class Meta:
        permissions = (
            ("admin_task", "Can manage users."),
        )
        
    user=models.OneToOneField(User)

