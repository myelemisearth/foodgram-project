from django.views.generic import DetailView, ListView

from django.contrib.auth import get_user_model

from .models import Recipe

User = get_user_model()

class Recipes(ListView):
    queryset = Recipe.objects.all()
    template_name = 'recipes/index.html'


class Recipe(DetailView):
    model = Recipe
    template_name = 'recipes/singlepage.html'


class RecipeEdit(DetailView):
    model = Recipe
    template_name = 'recipes/form_recipe.html'

class Basket(ListView):
    pass
