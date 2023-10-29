from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CommentForm
from .models import User, Listing, Bid, Comment, Category


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method != "POST":
        return render(request, "auctions/login.html")
    else:
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method != "POST":
        return render(request, "auctions/register.html")
    else:
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))


def listing_detail(request, pk):
    listing = Listing.objects.get(pk=pk)
    bids = Bid.objects.filter(listing=listing)
    comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment(
                author=comment_form.cleaned_data["author"],
                body=comment_form.cleaned_data["body"],
                listing=listing,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(listing=listing).order_by("-created_on")
    context = {
        "listing": listing,
        "comments": comments,
        "comment_form": CommentForm(),
        "bids": bids,
    }

    return render(request, "auctions/detail.html", context)


def category_index(request):
    categories = Category.objects.order_by("name")
    context = {
        "categories": categories,
    }

    return render(request, "auctions/category_index.html", context)


def listings_by_category(request, category):
    listings = Listing.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "listings": listings,
    }
    return render(request, "auctions/category.html", context)
