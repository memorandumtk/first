from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("", views.listings, name="listings"),
    path("listing/<int:listing_id>/", views.specific_listing, name="specific_listing"),
    path("tobid/<int:listing_id>/", views.to_bid, name="to_bid"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>/", views.watchlist_add, name="watchlist_add"),
    path("categories/", views.categories, name="categories"),
    path("create/", views.create_listing_view, name="create"), 
    path("to_close/<int:listing_id>/", views.to_close, name="to_close"), 
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
