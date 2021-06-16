from django import forms

from .models import EatingTimes, Ingredient, Recipe


class CreationRecipeForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(
        queryset=EatingTimes.objects.all(),
        required=False,
    )
    ingredient = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        required=False,
    )
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'tag', 'ingredient', 'cooking_time',)
