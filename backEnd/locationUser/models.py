from django.db import models
from django.db.models.fields import DecimalField
from authUser.models import CustomAccount


# Create your models here.
class LocationData(models.Model):
    user_id = models.ForeignKey(CustomAccount, on_delete=models.CASCADE)
    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)


class BluetoothData(models.Model):
    user_id = models.ForeignKey(CustomAccount, on_delete=models.CASCADE)
    devices_nearby = models.JSONField()
