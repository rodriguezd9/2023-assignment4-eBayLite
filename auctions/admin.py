from django.contrib import admin
from auctions.models import Bid, Category, Comment, Listing


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    pass
