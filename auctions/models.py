from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #MHB: Very elegant!
    watched_listings = models.ManyToManyField("Listing")


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    bidPrice = models.DecimalField(max_digits=10, decimal_places=2)
    #MHB: The related_name should be "listings" or "mylistings", so you can write: "user.my_listings.all()"
    #MHB: Why "settings.AUTH_USR_MODEL" rather than "User"?
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seller")
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    #MHB: I'd be consistent - either camelCase or underscores
    isListingActive = models.BooleanField(default=True)
    imageLink = models.URLField(max_length=200, null=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)
    #MHB:Ah, now I see the problem. The related_name should be "won_listings", but I think you cannot have
    #MHB: two different related_names to the same object. So you have "User" and "settings.AUTH_USER_MODEL" to 
    #MHB: get around the issue
    winner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="winner", null=True)

    def __str__(self):
        return f'{self.title} with current bid: {self.bidPrice}'


class Bid(models.Model):#
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
    #MHB: Pretty sure that you are using name as the PK, or at least you are assuming it's unique
    #MHB: Add those constraints here so db enforces this, and that somebody reading the code knows
    #MHB: what you are assuming
    name = models.CharField(max_length=40)

    class Meta:
        #MHB: I like the attention to detail!
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
