import io
import json

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import FileResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, TemplateView, UpdateView, View)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from foodgram.settings import (ABOUT_AUTHOR_TEXT, ABOUT_AUTHOR_TITLE,
                               ABOUT_TECH_TEXT, ABOUT_TECH_TITLE)

from .forms import CreationRecipeForm
from .models import (Basket, EatingTime, Favorite, Ingredient, Recipe,
                     RecipeIngredient, Subscription)

pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))

User = get_user_model()


class CheckDataCustomMixin:

    def check_data(self, data, model):
        if 'id' not in data:
            return JsonResponse(
                {'erorr': 'incorrect request'},
                status=400,
                safe=False
            )
        return get_object_or_404(model, id=data['id'])


class PrepareDataCustomMixin:

    def prepare_data(self, request):
        request.POST = request.POST.copy()
        ingredients = dict(
            value.split(';') for key, value in request.POST.dict().items()
            if key.startswith('ingredient'))
        for key in ingredients.keys():
            request.POST.update({'ingredient': key})
        return ingredients

    def create_recipes(self, ingredients, form):
        if ingredients:
            for item in form.cleaned_data['ingredient']:
                RecipeIngredient.objects.create(
                    recipe=self.object,
                    ingredient=item,
                    amount=ingredients[item.name])


class GetContextCustomMixin:

    def add_data_to_context(self, context):
        if self.request.user.is_authenticated:
            favorite_recipes = Recipe.objects.filter(
                favorite_user__user=self.request.user).values_list(
                    'id', flat=True)
            basket_recipes = Recipe.objects.filter(
                buyer__user=self.request.user).values_list('id', flat=True)
            context['basket_recipes'] = basket_recipes
            context['favorite_recipes'] = favorite_recipes
        tags = EatingTime.objects.all()
        context['tags'] = tags
        return context


class AboutView(TemplateView):
    template_name = 'recipes/about_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'author' in self.request.path:
            context['title'] = ABOUT_AUTHOR_TITLE
            context['text'] = ABOUT_AUTHOR_TEXT
        else:
            context['title'] = ABOUT_TECH_TITLE
            context['text'] = ABOUT_TECH_TEXT
        return context


class PurchaseView(LoginRequiredMixin, CheckDataCustomMixin, View):

    def get(self, request, *args, **kwargs):
        if kwargs['id']:
            relation = get_object_or_404(Basket, id=kwargs['id'])
            relation.delete()
        return redirect('recipes:recipe_basket')

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        recipe = self.check_data(data, Recipe)
        relation = False
        if recipe and not recipe.buyer.filter(
                user=request.user).exists():
            relation = Basket.objects.create(
                user=request.user, recipe=recipe)
        if relation:
            return JsonResponse(
                {'success': True},
                status=200,
                safe=False
            )
        return JsonResponse(
            {'success': False},
            status=404,
            safe=False
        )

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        recipe = self.check_data(data, Recipe)
        relation = get_object_or_404(
            Basket, recipe=recipe, user=request.user)
        relation.delete()
        return JsonResponse(
            {'success': True},
            status=200,
            safe=False
        )


class IngredientView(View):

    def get(self, request, *args, **kwargs):
        queryset = list(Ingredient.objects.filter(
            name__icontains=self.request.GET.get('query'))
            .annotate(dimension=F('unit'), title=F('name'))
            .values('title', 'dimension'))
        return JsonResponse(
            queryset,
            status=200,
            safe=False
        )


class FavoriteView(LoginRequiredMixin, CheckDataCustomMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        recipe = self.check_data(data, Recipe)
        relation = False
        if recipe and not recipe.favorite_user.filter(
                user=request.user).exists():
            relation = Favorite.objects.create(
                user=request.user,
                recipe=recipe
            )
        if relation:
            return JsonResponse(
                {'success': True},
                status=200,
                safe=False
            )
        return JsonResponse(
            {'success': False},
            status=404,
            safe=False
        )

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        recipe = self.check_data(data, Recipe)
        relation = get_object_or_404(
            Favorite, recipe=recipe, user=request.user)
        relation.delete()
        return JsonResponse(
            {'success': True},
            status=200,
            safe=False
        )


class SubscriptionView(LoginRequiredMixin, CheckDataCustomMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        relation = False
        author = self.check_data(data, User)
        if author != request.user and not author.following.filter(
                user=request.user).exists():
            relation = Subscription.objects.create(
                author=author, user=request.user)
        if relation:
            return JsonResponse(
                {'success': True},
                status=200,
                safe=False
            )
        return JsonResponse(
            {'success': False},
            status=404,
            safe=False
        )

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        author = self.check_data(data, User)
        relation = get_object_or_404(
            Subscription, author=author, user=request.user)
        relation.delete()
        return JsonResponse(
            {'success': True},
            status=200,
            safe=False)


class RecipeCreateView(LoginRequiredMixin, PrepareDataCustomMixin, CreateView):
    form_class = CreationRecipeForm
    success_url = reverse_lazy('recipes:index')
    template_name = 'recipes/form_recipe.html'

    def post(self, request, *args, **kwargs):
        self.ingredients = self.prepare_data(request)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        for item in form.cleaned_data['tags']:
            self.object.tags.add(item)
        self.create_recipes(self.ingredients, form)
        return HttpResponseRedirect(self.get_success_url())


class RecipeEditView(LoginRequiredMixin, PrepareDataCustomMixin, UpdateView):
    model = Recipe
    form_class = CreationRecipeForm
    success_url = 'recipes:recipe'
    template_name = 'recipes/form_recipe.html'

    def get_success_url(self):
        return reverse_lazy(
            self.success_url,
            kwargs={'pk': self.kwargs.get('pk')}
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
        self.ingredients = self.prepare_data(request)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        RecipeIngredient.objects.filter(recipe=self.object.id).delete()
        self.create_recipes(self.ingredients, form)
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


class ProfileRecipesListView(GetContextCustomMixin, ListView):
    paginate_by = 12
    template_name = 'recipes/author_recipe.html'

    def get_queryset(self):
        self.author = get_object_or_404(User, id=self.kwargs['pk'])
        tags = self.request.GET.getlist('tag')
        if tags:
            return Recipe.objects.filter(author=self.author).filter(
                tags__slug__in=tags).distinct()
        return Recipe.objects.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.add_data_to_context(context)
        if self.request.user.is_authenticated:
            context['following'] = self.author.following.filter(
                user=self.request.user).exists()
        context['author'] = self.author
        return context


class RecipeListView(GetContextCustomMixin, ListView):
    paginate_by = 12
    template_name = 'recipes/index.html'

    def get_queryset(self):
        tags = self.request.GET.getlist('tag')
        if tags:
            return Recipe.objects.filter(tags__slug__in=tags).distinct()
        return Recipe.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.add_data_to_context(context)


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/single_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            object = self.get_object()
            favorite_recipes = Favorite.objects.filter(
                recipe=object.id, user=self.request.user).exists()
            basket_recipes = Basket.objects.filter(
                recipe=object.id, user=self.request.user).exists()
            context['basket_recipes'] = basket_recipes
            context['favorite_recipes'] = favorite_recipes
            following = object.author.following.filter(
                user=self.request.user).exists()
            context['following'] = following
        return context


class BasketListView(LoginRequiredMixin, ListView):
    template_name = 'recipes/basket.html'
    context_object_name = 'basket'

    def get_queryset(self):
        return self.request.user.purchase.all()


class BasketDownloadView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        queryset = RecipeIngredient.objects.filter(
            recipe__buyer__user=request.user).prefetch_related('ingredient')
        value_for_file = self.get_value(queryset)
        return self.make_file(value_for_file)

    def get_value(self, data):
        ingredients = {}
        for item in data:
            if item.ingredient in ingredients:
                ingredients[item.ingredient] += item.amount
            else:
                ingredients[item.ingredient] = item.amount
        return ingredients

    def make_file(self, data):
        buffer = io.BytesIO()
        file = canvas.Canvas(buffer)
        file.setFont('Verdana', 8)
        pos_x, pos_y, count = 30, 830, 1
        for key, value in data.items():
            if count == 56:
                file.showPage()
            pos_y -= 15
            file.drawString(
                pos_x, pos_y,
                f'{key.name} : {value} {key.unit}'.encode()
            )
            count += 1
        file.showPage()
        file.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='purchases.pdf')


class FollowListView(LoginRequiredMixin, ListView):
    paginate_by = 6
    model = Recipe
    template_name = 'recipes/follow.html'

    def get_queryset(self):
        return User.objects.prefetch_related('recipes').filter(
            following__user=self.request.user)


class FavoriteListView(LoginRequiredMixin, GetContextCustomMixin, ListView):
    paginate_by = 12
    model = Recipe
    template_name = 'recipes/favorite.html'

    def get_queryset(self):
        tags = self.request.GET.getlist('tag')
        if tags:
            return Recipe.objects.filter(
                favorite_user__user=self.request.user).filter(
                    tags__slug__in=tags).distinct()
        return Recipe.objects.filter(favorite_user__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.add_data_to_context(context)
