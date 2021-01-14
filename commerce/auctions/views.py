from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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
        return render(request, "auctions/create_listing.html")
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        price = int(request.POST["price"])
        image = request.POST["url"]
        category = request.POST["category"]
        user = request.user

        new_listing = Listing(
            user=user, title=title, description=description, price=price, image=image, category=category
        )
        new_listing.save()
        return HttpResponseRedirect(reverse("listing", args={new_listing.id}))

def listing(request, listing_id):
    if request.method == "GET":
        listing = Listing.objects.get(pk=listing_id)
        all_comments = Comment.objects.get()
        
        #condition for "posted by" information in template
        if listing.user == request.user:
            return render(request, "auctions/listing.html",{
                "listing": listing,
                "current_user": request.user,
                "category": listing.get_category_display()
            })
        else:
            return render(request, "auctions/listing.html",{
                "listing": listing,
                "category": listing.get_category_display()
            })


def watchlist(request):
    return render(request, "auctions/watchlist.html")
