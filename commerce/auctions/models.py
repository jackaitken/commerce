from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORIES = (
    ('N', 'None'),
    ('E', 'Electronics'),
    ('H', 'Home'),
    ('F', 'Fashion'),
    ('T', 'Toys'),
    ('A', 'Automobiles'),
    ('O', 'Other')
)

class User(AbstractUser):
    watchlist = models.ManyToManyField('Watchlist', related_name="user_watchlist")

class Bid(models.Model):
    bids = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    title = models.CharField(max_length=50, null=True)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user_comments")
 
class Listing(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=False)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    image = models.URLField(null=True, blank=True, verbose_name="image")
    comment = models.ManyToManyField('Comment', related_name="listing_comment")
    category = models.CharField(max_length=1, choices=CATEGORIES, null=True)

    def __str__(self):
        return f"{self.title}, posted by {self.user}"

class Watchlist(models.Model):
    listing = models.ManyToManyField(Listing, related_name="listing_watchlist")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_watchlist")

    def __str__(self):
        return f"{self.user}'s watchlist"
