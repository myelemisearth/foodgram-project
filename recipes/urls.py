from django.urls import path

from . import views

urlpatterns = [
    path('basket/',
         views.Recipes.as_view(),
         name='basket'),
    path('recipes/<int:pk>/',
         views.Recipe.as_view(),
         name='recipe'),
    path('',
         views.Recipes.as_view(),
         name='index'),
]
