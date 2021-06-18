from django.contrib.auth import get_user_model
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import CreationRecipeForm
from .models import Ingredient, Recipe

User = get_user_model()


class GetIngredient(ListView):

    def get(self, request, *args, **kwargs):
        queryset = (Ingredient.objects.filter(
            name__icontains=self.request.GET.get('query'))
            .annotate(dimension=F('unit'), title=F('name'))
            .values('title', 'dimension'))
        return JsonResponse(list(queryset), status=200, safe=False)


class CreateRecipe(CreateView):
    form_class = CreationRecipeForm
    success_url = reverse_lazy('recipes:index')
    template_name = 'recipes/form_recipe.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        print(form.cleaned_data)
        for item in form.cleaned_data['tag']:
            self.object.tag.add(item)
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            print('Form is valid')
            return self.form_valid(form)
        else:
            print('Form is not valid')
            return self.form_invalid(form)


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
