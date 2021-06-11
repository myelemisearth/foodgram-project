from django.contrib import admin

from .models import EatingTimes, Ingredient, Recipe, RecipeIngredient


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author', 'description')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


class EatingTimesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(EatingTimes, EatingTimesAdmin)
