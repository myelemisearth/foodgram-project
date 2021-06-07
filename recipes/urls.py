from django.urls import path

from . import views

urlpatterns = [
    path('basket/',
         views.Recipes.as_view(),
         name='basket'),
    path('',
         views.Recipes.as_view(),
         name='index'),
]
