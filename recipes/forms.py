from django import forms

from .models import EatingTime, Ingredient, Recipe


class CreationRecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=EatingTime.objects.all(),
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
        fields = ('title', 'description', 'tags', 'cooking_time', 'image')
