from django.urls import path

from . import views

urlpatterns = [
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
