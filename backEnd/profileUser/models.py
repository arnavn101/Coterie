from django.db import models
from authUser.models import CustomAccount
import os


class ProfileUser(models.Model):
    user_id = models.ForeignKey(CustomAccount, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to=os.path.join('profileUser', 'user_profile_pictures'))
    categories_selected = models.JSONField()
