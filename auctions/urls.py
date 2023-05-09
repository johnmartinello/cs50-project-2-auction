from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closedListings", views.closedListings, name="closedListings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categoryListing", views.categoryListing, name="categoryListing"),
    path("listing/<int:id>", views.listingView, name="listing"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("watchList", views.watchList, name="watchList"),

]
