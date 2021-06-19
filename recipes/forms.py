from django import forms
from django.http import request

from .models import EatingTimes, Ingredient, Recipe, RecipeIngredient


class CreationRecipeForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(
        queryset=EatingTimes.objects.all(),
        required=False,
        to_field_name='slug',
    )
    ingredient = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        required=False,
        to_field_name='name',
    )

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'tag', 'cooking_time', 'ingredient')
