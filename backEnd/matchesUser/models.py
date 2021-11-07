from django.db import models
from authUser.models import CustomAccount


class Matches(models.Model):
    outgoing_user_id = models.ForeignKey(CustomAccount, on_delete=models.CASCADE, related_name='outgoing_user_id')
    incoming_user_id = models.ForeignKey(CustomAccount, on_delete=models.CASCADE, related_name='incoming_user_id')
    # Match_status: -1 for Rejected, 0 for Pending, 1 for Accepted
    match_status = models.IntegerField(default=0)
