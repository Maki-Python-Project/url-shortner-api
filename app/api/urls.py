from django.urls import path

from . import views


urlpatterns = [
    path('shorten/', views.MakeshortUrl.as_view()),
    path('<str:shorturl>', views.RedirectUrl.as_view()),
]
