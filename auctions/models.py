from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.utils import timezone

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    pass

class Category(models.Model):
    # id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15)
    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=15)
    description = models.CharField(max_length=100)
    starting_bid = models.IntegerField()
    # current_price = models.ForeignKey(Bidmodel, on_delete=models.CASCADE, null=True, related_name="listing_currentprice")
    image = models.ImageField(upload_to='images', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="category_name")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    isactive = models.BooleanField(null=True, default=True)

    def __str__(self):
        return f"{self.id}: {self.title}: {self.description}: {self.starting_bid}: {self.image}: {self.category}: {self.isactive}: {self.owner}"
    class Meta:
        ordering = ['-created_at']

class Bidmodel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
        )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, null=True, blank=True
        )
    current_bid = models.IntegerField()
    def __str__(self):
        return f"{self.current_bid}: {self.user} :{self.listing}"


class Watchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # item = models.ManyToManyField(Listing, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="watchlist_user"
    )
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, null=True, related_name="watching_item"
    )
    def __str__(self):
        return f"{self.user} 's WatchList, {self.item}: {self.id}"

class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="comment_user"
    )
    listing = models.ForeignKey(
       Listing, on_delete=models.CASCADE, null=True, related_name="comment_listing"
    )
    commentmessage = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"{self.user} 's comment on {self.listing}"
    
