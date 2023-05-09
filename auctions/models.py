from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime




class User(AbstractUser):
    pass

class Categories(models.Model):
    categoriesName = models.CharField(max_length=32)
    
    def __str__(self):
        return self.categoriesName

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    bid = models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    
    def __str__(self):
        return f"{self.bid} by {self.bidder}"


class Listing(models.Model):
    title = models.CharField(max_length=32, null=True)
    description = models.CharField(max_length=256, null=True)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True)
    time = models.DateTimeField(default=timezone.now)
    imageURL = models.CharField(max_length=512, null=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE,blank=True, null=True, related_name="category")
    creator = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="user")
    watchList = models.ManyToManyField(User, blank=True, null=True, related_name="watchlistUser")

    def __str__(self):
        return self.title
    
class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="commenter")
    comment = models.CharField(max_length=128, null=True, blank=True)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="auction" )
    
    def __str__(self):
        return f"{self.comment} by {self.commenter} on {self.auction}"
    