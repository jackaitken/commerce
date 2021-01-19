from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import CreateListing, AddComment

from .models import User, Listing, Bid, Comment, Watchlist


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

@login_required
def create_listing(request):
    if request.method == "GET":
        form = CreateListing()
        return render(request, "auctions/create_listing.html", {
            "form": form
        })

    # Get listing information from form
    else:
        new_listing = CreateListing(request.POST)
        if new_listing.is_valid():
            add_listing = new_listing.save(commit=False)
            add_listing.user = request.user
            add_listing.save()
            return HttpResponseRedirect(reverse("listing", args={add_listing.id}))

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    current_user = request.user
    if request.method == "GET":
        comments = listing.comment.all()
        comment_form = AddComment()
        return render(request, "auctions/listing.html",{
            "listing": listing,
            "current_user": current_user,
            "category": listing.get_category_display(),
            "comments": comments,
            "comment_form": comment_form
        })
        
    else:
        # Checks if POST is for a comment or watchlist 
        if 'title' in request.POST:
            comment = AddComment(request.POST)
            if comment.is_valid():
                new_comment = comment.save(commit=False)
                new_comment.user = current_user
                new_comment.save()
                listing.comment.add(new_comment)
        else:
            #struggling with how to add to watchlist
            try:
                user_watchlist = Watchlist.objects.get(pk=current_user.id)
                watchlist_add = listing.save(commit=False)
                watchlist_add.save()
                user_watchlist.listing.add(watchlist_add)
            except ObjectDoesNotExist:
                new_watchlist = Watchlist(user=current_user)
                new_watchlist.save()
                new_watchlist.listing.add(listing)
                
        return HttpResponseRedirect(reverse("listing", args={listing.id}))

@login_required
def watchlist(request):
    watchlist_items = request.user.user_watchlist

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist_items
    })
