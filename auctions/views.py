from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required

from .models import User, Categories, Listing, Bid, Comments


def index(request):
    allListing = Listing.objects.filter(active=True)
    listofcategories = Categories.objects.all()
    return render(request, "auctions/index.html",{
        "listings": allListing,
        "categories":listofcategories,
        "active": True,
        "watchlist": False
    })
    
def closedListings(request):
    allListing = Listing.objects.filter(active=False)
    listofcategories = Categories.objects.all()
    return render(request, "auctions/index.html",{
        "listings": allListing,
        "categories":listofcategories,
        "active": False,
        "watchlist": False
    })

def listingView(request, id):
    listingInfo = Listing.objects.get(pk=id)
    getComments = Comments.objects.filter(auction=listingInfo)
    inWatchlist = request.user in listingInfo.watchList.all()
    
    
    if listingInfo.active == False:
        return render(request, "auctions/listing.html",{
        "listing": listingInfo,
        "comments": getComments,
        "active": False,
    
        })
    
    else:
        return render(request, "auctions/listing.html",{
        "listing": listingInfo,
        "comments": getComments,
        "active": True,
        "inWatchlist": inWatchlist
        })


def categoryListing(request):
    if request.method == "POST":
        category_get = request.POST["category"]
        category = Categories.objects.get(categoriesName=category_get)
        allListing = Listing.objects.filter(active=True, category=category)
        listofcategories = Categories.objects.all()
        return render(request, "auctions/index.html",{
            "listings": allListing,
            "categories":listofcategories,
            "active": True
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
    

def create(request):
    user = request.user    
    
    #if requesting the page, return the forms page
    if request.method =="GET":
        listofcategories = Categories.objects.all()
        return render(request, "auctions/create.html",{
         "categories":listofcategories,
     })
    
    #if sending data, save all the inputs to the sql table Listing (as is the models.py class])
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        starterBid = request.POST["starterBid"]
        imageURL = request.POST["imageurl"]
        category = request.POST["category"]
        categoryInfo = Categories.objects.get(categoriesName=category)
        
        addBid = Bid(
            bid = float(starterBid),
            bidder = user,
        )
        addBid.save()
       
        createListing = Listing(
            title = title,
            description = description,
            imageURL = imageURL,
            active = True,
            category = categoryInfo,
            creator= user,
            price = addBid
            )
        createListing.save()
        
        #redirect to the index page
        return HttpResponseRedirect(reverse(index))
    

def addBid(request, id):
    
    newBid = request.POST["newBid"]
    listingInfo = Listing.objects.get(pk=id)
    comments = Comments.objects.filter(auction=listingInfo)
    
    #checks if new bid is greater the the current price. If so, creates a new bid and replace the current one
    if float(newBid) > listingInfo.price.bid and listingInfo.active == True and Listing.creator and request.user != listingInfo.creator:
        updateBid = Bid(
            bid = float(newBid),
            bidder = request.user
        )
        updateBid.save()
        
        listingInfo.price = updateBid
        listingInfo.save()
    
        return render(request, "auctions/listing.html", {
            "listing": listingInfo,
            "alert": "New bid placed!",
            "update": True,
            "active": True,
            "comments": comments
        })

    else:
        return render(request, "auctions/listing.html", {
            "listing": listingInfo,
            "alert": "Bid failed!",
            "update": False,
            "active": True,
            "comments": comments
        })

def addComment(request, id):
    listingInfo = Listing.objects.get(pk=id)
    newComment = request.POST["addComment"]
    
    addComment = Comments(
        commenter = request.user,
        comment = newComment,
        auction = listingInfo
    )
    addComment.save()
    comments = Comments.objects.filter(auction=listingInfo)
    
    if Listing.active == False:
       return render(request, "auctions/listing.html",{
        "listing": listingInfo,
        "comments": comments,
        
        }) 
    
    else:
        return render(request, "auctions/listing.html",{
        "listing": listingInfo,
        "comments": comments,
        "active": True 
        })
    
def closeAuction(request,id):
    listingInfo = Listing.objects.get(pk=id)
    getComments = Comments.objects.filter(auction=listingInfo)
    close = request.POST['closeAuction']
    comments = Comments.objects.all()
    
    if request.user == listingInfo.creator:
        listingInfo.active = False
        listingInfo.save()
        
        return render(request, "auctions/listing.html",{
        "listing": listingInfo,
        "comments": comments,
        "closed": True,
        "message": "Auction is closed!"   
    })
        
    else:
        return render(request, "auctions/listing.html",{
            "listing": listingInfo,
            "comments": comments,
            "closed": False,
            "active": True,
            "message": "Failed action! You must be the auction creator to be able to close it!"     
        }) 
        
def addWatchlist(request,id):
    listingInfo = Listing.objects.get(pk=id)
    user = request.user
    listingInfo.watchList.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
    

def removeWatchlist(request,id):
    listingInfo = Listing.objects.get(pk=id)
    user = request.user
    listingInfo.watchList.remove(user)
    
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def watchList(request):
    user = request.user
    allListings = user.watchlistUser.all()
    listofcategories = Categories.objects.all()
    
    return render(request, "auctions/index.html",{
        "listings": allListings,
        "categories":listofcategories,
        "active": True,
        "watchlist": True
    })