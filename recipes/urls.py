from django.urls import path
from . import views

urlpatterns = [
    path('recipes/',
         views.Recipes.as_view(),
         name='index'),
    path('basket/',
         views.Recipes.as_view(),
         name='basket'),
]
