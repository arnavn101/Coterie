from django.db import models
from authUser.models import CustomAccount
from profileUser.interests_list import interests_dict
import copy


def returnListDictInterests():
    return copy.deepcopy(interests_dict)


def returnEmptyDict():
    return copy.deepcopy({})


class InterestProfile(models.Model):
    user_id = models.ForeignKey(CustomAccount, on_delete=models.CASCADE)
    # Ex: ['Printing': 0, 'Gaming': 0, ...]
    dict_interests_weights = models.JSONField(default=returnListDictInterests)


class AlgoIDToUserID(models.Model):
    mapping = models.JSONField(default=returnEmptyDict)
