from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:pk>/", views.listing_detail, name="listing_detail"),
    path("category/<category>/", views.listing_category, name="listing_category"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register")
]
