from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateListing, AddComment

from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

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
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
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
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "GET":
        form = CreateListing()
        return render(request, "auctions/create_listing.html", {
            "form": form
        })

    else:
        new_listing = CreateListing(request.POST)
        if new_listing.is_valid():
            add_listing = new_listing.save(commit=False)
            add_listing.user = request.user
            add_listing.save()
            return HttpResponseRedirect(reverse("listing", args={add_listing.id}))

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "GET":
        comments = listing.comment.all()
        comment_form = AddComment()
        return render(request, "auctions/listing.html",{
            "listing": listing,
            "current_user": request.user,
            "category": listing.get_category_display(),
            "comments": comments,
            "comment_form": comment_form
        })
        
    else:
        comment = AddComment(request.POST)
        if comment.is_valid():
            new_comment = comment.save(commit=False)
            new_comment.user = request.user
            new_comment.save()
            listing.comment.add(new_comment)

        return HttpResponseRedirect(reverse("listing", args={listing.id}))

def watchlist(request):
    return render(request, "auctions/watchlist.html")
