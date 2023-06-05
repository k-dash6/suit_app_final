from django.db import models
from custom_auth.models import User

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=256)
    # description = models.TextField()