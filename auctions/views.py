from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import *
from .models import User, Listing, Watchlist, Category


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("listings"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return render(request, "auctions/login.html")


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
        return HttpResponseRedirect(reverse("listings"))
    else:
        return render(request, "auctions/register.html")

def listings(request):
    listings = Listing.objects.all()
    bids = Bidmodel.objects.all()
    return render(request, "auctions/listing.html", {
        "listings": listings,
        "bids" : bids
    })

def specific_listing(request, listing_id):
    try:
        getlisting = Listing.objects.get(id=listing_id)
        watchlist = Watchlist.objects.filter(user=request.user, item=getlisting)
        bid_form = BidForm()
        isowner = request.user == getlisting.owner
        requestuser = request.user
        getcomment = Comment.objects.all()
        try:
            bidinfo = Bidmodel.objects.get(listing=listing_id)
        except:
            bidinfo = 0
    except Listing.DoesNotExist:
        raise Http404(" not found.")
    if request.method == "POST":
        form_c = CommentForm(request.POST)
        if form_c.is_valid():
            tocomment = form_c.save()
            tocomment.listing = getlisting
            tocomment.user = request.user
            tocomment.save()
            return redirect("specific_listing", listing_id)
    form_c = CommentForm()
    return render(request, "auctions/specific_listing.html", {
        "listing": getlisting,
        "watchlist": watchlist,
        "bid_form" : bid_form,
        "bidinfo" : bidinfo,
        "isowner" : isowner,
        "requestuser" : requestuser,
        "form_c" : form_c,
        "getcomment" : getcomment,
    })

@login_required
def to_bid(request, listing_id):
    if request.method == "POST":
        form_b = BidForm(request.POST)
        getlisting = Listing.objects.get(id=listing_id)
        isexsitedbid = Bidmodel.objects.filter(listing=listing_id).count()
        isowner = request.user == getlisting.owner
        if form_b.is_valid():
            if isexsitedbid == 0:
                    updatebid = form_b.save()
                    updatebid.user = request.user
                    updatebid.listing = getlisting
                    updatebid.save() 
            else:                  
                try:
                    getcurrentprice = Bidmodel.objects.get(listing=getlisting)
                    addedbid=request.POST["current_bid"]
                    if int(addedbid) > getcurrentprice.current_bid:
                        getcurrentprice.delete()
                        updatebid = form_b.save()
                        updatebid.user = request.user
                        updatebid.listing = getlisting
                        updatebid.save()
                    else:
                        messages.error(request, "Your bid is invalid")
                except:
                    messages.error(request, "Error is occured")
            return HttpResponseRedirect(reverse("listings"))
    bid_form = BidForm()
    print(bid_form)
    return render(request, 'auctions/specific_listing.html', {
        "bid_form": bid_form,
    })

@login_required
def to_close(request, listing_id):
    getlisting = Listing.objects.get(id=listing_id)
    getowner = request.user
    if request.method == "POST":
        if getowner == getlisting.owner:
            getlisting.isactive = "False"
            getlisting.save()
            messages.success(request, "Your auction is closed")
    return HttpResponseRedirect(reverse('listings'))

@login_required
def categories(request):
    form_cat = CategoryForm(request.POST or None)
    if request.method == "POST":
        form_cat = CategoryForm(request.POST)
        if form_cat.is_valid():
            form_cat.save()
            return HttpResponseRedirect(reverse('listings'))
    return render(request, 'auctions/categories.html', {
        "form_cat": form_cat,
    })

@login_required
def create_listing_view(request):
    if request.method == "POST":
        form_l = ListingForm(request.POST, request.FILES)
        if form_l.is_valid():
            createlisting = form_l.save()
            createlisting.owner = request.user
            createlisting.save()
            return HttpResponseRedirect(reverse('listings'))
    else:
        listing_form = ListingForm()
    return render(request, 'auctions/create.html', {
        "listing_form": listing_form,
    })


def watchlist(request):
    watch_lists = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', {
        'watch_lists': watch_lists
    }) 

def watchlist_add(request, listing_id):
    item_to_save = Listing.objects.get(id=listing_id)
    watch_list = Watchlist.objects.filter(user=request.user, item=item_to_save)
    # Check if the item already exists in that user watchlist
    if watch_list.exists():
        watch_list.delete()
        messages.add_message(request, messages.ERROR, "You already have it in your watchlist.")
        return HttpResponseRedirect(reverse('watchlist'))
        # return render(request, 'auctions/specific_listing.html')  
    # Get the user watchlist or create it if it doesn't exists
    else:
        watch_list, created = Watchlist.objects.get_or_create(user=request.user, item=item_to_save)
        watch_list.save()
        messages.success(request, 'Successfully added to your watchlist')
        return HttpResponseRedirect(reverse('watchlist'))




