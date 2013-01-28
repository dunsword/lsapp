from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    class Meta:
        permissions = (
            ("admin_task", "Can manage users."),
        )
        
    user=models.OneToOneField(User)
