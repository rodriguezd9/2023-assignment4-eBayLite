from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CommentForm, ListingForm, BidForm
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
    comments = Comment.objects.filter(listing=listing).order_by("-created_on")
    bids = Bid.objects.filter(listing=listing).order_by("-amount")
    #MHB: This variable is set to hold a User object; the default should be None rather than an empty string
    highest_bidder = ""
    user = request.user

    if bids.count() != 0:
        highest_bidder = bids[0].bidder

    if request.method == "POST" and "close_auction" in request.POST:
        if highest_bidder == "":
            listing.winner = request.user
        else:
            listing.winner = highest_bidder
        listing.isListingActive = False
        listing.save()
        #MHB: Why path_info rather than reverse('listing' pk=...)?
        return HttpResponseRedirect(request.path_info)

    if request.method == "POST" and "add_to_watchlist" in request.POST:
        user.watched_listings.add(listing)
        return HttpResponseRedirect(request.path_info)

    if request.method == "POST" and "remove_from_watchlist" in request.POST:
        user.watched_listings.remove(listing)
        return HttpResponseRedirect(request.path_info)

    if request.method == "POST" and "comment_submit" in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment(
                author=request.user,
                body=comment_form.cleaned_data["body"],
                listing=listing,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    if request.method == "POST" and listing.isListingActive and "bid_submit" in request.POST:
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            if bid_form.cleaned_data["amount"] <= listing.bidPrice:
                context = {
                    "listing": listing,
                    "comments": comments,
                    "comment_form": CommentForm(),
                    "highest_bidder": highest_bidder,
                    #MHB: This should be bid_form so other error message are captured, and
                    #MHB:   whatever user typed in stays around
                    "bid_form": BidForm(),
                    "user": user,
                    "error": "Bid amount too low",
                }
                return render(request, "auctions/detail.html", context)
            else:
                bid = Bid(
                    bidder=request.user,
                    amount=bid_form.cleaned_data["amount"],
                    listing=listing,
                )
                bid.save()
                listing.bidPrice = bid.amount
                listing.save()
                return HttpResponseRedirect(request.path_info)

    context = {
        "listing": listing,
        "comments": comments,
        "comment_form": CommentForm(),
        "highest_bidder": highest_bidder,
        "bid_form": BidForm(),
        "user": user,
    }

    return render(request, "auctions/detail.html", context)


def category_index(request):
    categories = Category.objects.order_by("name")
    context = {
        "categories": categories,
    }

    return render(request, "auctions/category_index.html", context)


def listings_by_category(request, category):
    #MHB: I'm not a fan of using the name of the category rather than an id. 
    #MHB: If you use the name, you are assuming it's unique... so in the definition
    #MHB: of Category you need to add a unique=True constraint
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
            #MHB: Why not: 
            #MHB    listing = form.save(commit=False) 
            #MHB    list.seller = request.user
            listing = Listing(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                bidPrice=form.cleaned_data["bidPrice"],
                seller=request.user,
                imageLink=form.cleaned_data["imageLink"],
                category=form.cleaned_data["category"],
            )
            listing.save()
            if listing.imageLink == "":
                listing.imageLink = "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"
                listing.save()
            return HttpResponseRedirect(reverse('listing_detail', args=[listing.id]))
    context = {
        "form": form,
    }
    return render(request, "auctions/new_listing.html", context)


def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        listings = (Listing.objects.filter(
            user=request.user.id
        ).order_by("-created_on"))
        context = {
            "listings": listings,
        }
        return render(request, "auctions/watchlist.html", context)
