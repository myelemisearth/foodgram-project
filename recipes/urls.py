from django.urls import path

from . import views

urlpatterns = [
    path('basket/',
         views.BasketView.as_view(),
         name='basket'),
    path('recipes/create_recipe/',
         views.RecipeCreateView.as_view(),
         name='create_recipe'),
    path('recipes/<int:pk>/',
         views.RecipeDetailView.as_view(),
         name='recipe'),
    path('recipes/<int:pk>/edit/',
         views.RecipeEditView.as_view(),
         name='recipe_edit',),
    path('recipes/<int:pk>/delete/',
         views.RecipeDeleteView.as_view(),
         name='recipe_delete',),
    path('ingredients/',
         views.GetIngredient.as_view(),
         name='ingredients'),
    path('profile/<int:pk>/',
         views.ProfileView.as_view(),
         name='profile'),
    path('',
         views.RecipesListView.as_view(),
         name='index'),
]
