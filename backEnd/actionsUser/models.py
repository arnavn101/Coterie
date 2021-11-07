from django.db import models
from authUser.models import CustomAccount
import copy

def returnBoilerplateList():
    return copy.deepcopy([])

class ActionsUser(models.Model):
    user_id = models.ForeignKey(CustomAccount, on_delete=models.CASCADE)
    match_approved = models.JSONField(default=returnBoilerplateList)
    match_received = models.JSONField(default=returnBoilerplateList)