from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watched_listings = models.ManyToManyField("Listing")


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    bidPrice = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    isListingActive = models.BooleanField(default=True)
    imageLink = models.URLField(max_length=200, null=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.title} with current bid: {self.bidPrice}'


class Bid(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.amount} for {self.listing} on {self.created_on}'


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} on "{self.listing}"'


class Category(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
