from django.urls import path

from . import views

urlpatterns = [
    path('basket/',
         views.Recipes.as_view(),
         name='basket'),
    path('recipes/create_recipe/',
         views.CreateRecipe.as_view(),
         name='create_recipe'),
    path('recipes/<int:pk>/',
         views.Recipe.as_view(),
         name='recipe'),
    path('recipes/<int:pk>/edit/',
         views.RecipeEdit.as_view(),
         name='recipe_edit',),
    path('',
         views.Recipes.as_view(),
         name='index'),
]
