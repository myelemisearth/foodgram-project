from django.contrib.auth import get_user_model
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import CreationRecipeForm
from .models import Ingredient, Recipe, RecipeIngredient

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

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        self.ingredient = dict(
            value.split(',') for key, value in request.POST.dict().items()
            if key.startswith('ingredient'))
        for key in self.ingredient.keys():
            request.POST.update({'ingredient': key})
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        for item in form.cleaned_data['tag']:
            self.object.tag.add(item)
        for item in form.cleaned_data['ingredient']:
            if item.name in self.ingredient:
                RecipeIngredient.objects.create(
                    recipe=self.object,
                    ingredient=item,
                    amount=self.ingredient[item.name])
        return HttpResponseRedirect(self.get_success_url())


class Recipes(ListView):
    paginate_by = 12
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
