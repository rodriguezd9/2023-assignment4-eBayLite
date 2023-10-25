from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    bidPrice = models.DecimalField(max_digits=10, decimal_places=2)
    # TODO: Change seller to automatically pick up logged in user's name
    seller = models.CharField(max_length=60)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    close_on = models.DateTimeField()
    # TODO: Consider creating folder structure for user/listing
    imageLink = models.URLField(max_length=200, )
    categories = models.ManyToManyField("Category", related_name="listings")

    def __str__(self):
        return f'{self.title} with current bid: {self.bidPrice}'


class Bid(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.amount} for {self.listing} on {self.created_on}'


class Comment(models.Model):
    # TODO: Change author to automatically pick up logged in user's name
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} on "{self.listing}"'


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
