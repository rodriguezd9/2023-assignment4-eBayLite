from django.urls import path

from . import views

urlpatterns = [
    #MHB: Good choices of names. it's pretty sophisticated to have a single path 
    #MHB    for the listing, and then look at which button was clicked to determine
    #MHB    the action. But you could argue that a single "SAVE" button is better than a 
    #MHB    a "SUBMIT BID", "SUBMIT COMMENT". Arguable
    path("", views.index, name="index"),
    path("new_listing/", views.new_listing, name="new_listing"),
    path("listing/<int:pk>/", views.listing_detail, name="listing_detail"),
    path("category/<category>/", views.listings_by_category, name="listings_by_category"),
    path("category_index/", views.category_index, name="category_index"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register")
]
