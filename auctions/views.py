from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CommentForm, ListingForm
from .models import User, Listing, Bid, Comment, Category


def index(request):
    listings = Listing.objects.filter(isListingActive=True).order_by("-created_on")
    context = {
        "listings": listings
    }
    return render(request, "auctions/index.html", context)


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
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment(
                author=request.user,
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
        category__name=category, isListingActive=True
    ).order_by("-created_on")
    context = {
        "category": category,
        "listings": listings,
    }
    return render(request, "auctions/category.html", context)


def new_listing(request):
    form = ListingForm()
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = Listing(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                bidPrice=form.cleaned_data["bidPrice"],
                seller=request.user,
                imageLink=form.cleaned_data["imageLink"],
                category=form.cleaned_data["category"]
            )
            listing.save()
            if listing.imageLink == "":
                listing.imageLink = "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"
            listing.save()
            return HttpResponseRedirect("../listing/" + str(listing.id))
    context = {
        "form": form,
    }
    return render(request, "auctions/new_listing.html", context)
