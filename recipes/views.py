from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import CreationRecipeForm
from .models import Ingredient, Recipe, RecipeIngredient

User = get_user_model()


class GetIngredient(TemplateView):

    def get(self, request, *args, **kwargs):
        queryset = list(Ingredient.objects.filter(
            name__icontains=self.request.GET.get('query'))
            .annotate(dimension=F('unit'), title=F('name'))
            .values('title', 'dimension'))
        return JsonResponse(queryset, status=200, safe=False)


class RecipeCreateView(LoginRequiredMixin, CreateView):
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
        return super(RecipeCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        for item in form.cleaned_data['tag']:
            self.object.tag.add(item)
        for item in form.cleaned_data['ingredient']:
            RecipeIngredient.objects.create(
                recipe=self.object,
                ingredient=item,
                amount=self.ingredient[item.name])
        return HttpResponseRedirect(self.get_success_url())


class ProfileView(DetailView):
    model = User
    template_name = 'recipes/author_recipe.html'


class RecipeListView(ListView):
    paginate_by = 12
    #queryset = Recipe.objects.all()
    template_name = 'recipes/index.html'

    def get_queryset(self):
        tag = self.request.GET.get('tag')
        if tag:
            return Recipe.objects.filter(tag__slug=tag)
        return Recipe.objects.all()


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/single_page.html'


class RecipeEditView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = CreationRecipeForm
    success_url = 'recipes:recipe'
    template_name = 'recipes/form_recipe_change.html'

    def get_success_url(self):
        return reverse_lazy(
            self.success_url,
            kwargs={'pk':self.kwargs.get('pk')}
        )
    
    def get(self, request, *args, **kwargs):
        recipe = self.get_object()
        if recipe.author != request.user:
            return HttpResponseRedirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        if recipe.author != request.user:
            return HttpResponseRedirect(self.get_success_url())
        request.POST = request.POST.copy()
        self.ingredient = dict(
            value.split(',') for key, value in request.POST.dict().items()
            if key.startswith('ingredient'))
        for key in self.ingredient.keys():
            request.POST.update({'ingredient': key})
        return super(RecipeEditView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if self.ingredient:
            for item in form.cleaned_data['ingredient']:
                RecipeIngredient.objects.update_or_create(
                    recipe=self.object,
                    ingredient=item,
                    defaults={'amount': self.ingredient[item.name]})
        return HttpResponseRedirect(self.get_success_url())


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes:index')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.author == request.user:
            self.object.delete()
        return HttpResponseRedirect(success_url)


class BasketView(ListView):
    pass
