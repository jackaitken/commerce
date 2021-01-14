from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=16)

class Bid(models.Model):
    bids = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default="You must provide a description")
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    category = models.CharField(max_length=100)
    image = models.URLField()

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    comment = models.CharField(max_length=200)
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")



