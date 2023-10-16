from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing:
    def __init__(self, title, description, starting_bid, image_link, category, active):
        self.title = title
        self.description = description
        self.startingBid = starting_bid
        self.imageLink = image_link
        self.category = category
        self.active = active



class Bid:
    pass


class Comment:
    pass


class Category:
    pass
