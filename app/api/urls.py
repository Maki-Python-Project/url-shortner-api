from django.urls import path

from . import views


urlpatterns = [
    path('shorten/', views.MakeshortUrl.as_view()),
    path('<str:shorturl>', views.RedirectUrl.as_view()),
    path('shortened-urls-count/', views.get_count_all_shortened_url),
    path('the-most-popular/', views.TheMostPopularUrl.as_view()),
]
