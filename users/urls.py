from django.urls import path

from . import views

urlpatterns = [
    path('registration/',
         views.Register.as_view(),
         name='registration'),
]