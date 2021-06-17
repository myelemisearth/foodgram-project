from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.http import JsonResponse
from django.core import serializers

from .forms import CreationRecipeForm
from .models import Ingredient, Recipe

User = get_user_model()


class GetIngredient(ListView):
    queryset = Ingredient.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = serializers.serialize('json', queryset)
        return JsonResponse(data, status=200, safe=False)


class CreateRecipe(CreateView):
    form_class = CreationRecipeForm
    success_url = reverse_lazy('recipes:index')
    template_name = 'recipes/form_recipe.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        for item in form.cleaned_data['tag']:
            self.object.tag.add(item)
        return HttpResponseRedirect(self.get_success_url())


class Recipes(ListView):
    paginate_by = 10
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
