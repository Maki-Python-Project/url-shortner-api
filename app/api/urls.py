from django.urls import path

from . import views


urlpatterns = [
    path('shorten/', views.create_shorturl),
    path('<str:shorturl>', views.redirect_shorturl),
    path('shortened-urls-count/', views.get_count_all_shortened_url),
    path('the-most-popular/', views.get_the_most_popular),
]
