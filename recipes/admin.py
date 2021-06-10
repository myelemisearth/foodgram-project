from django.contrib import admin

from .models import Ingredient, Recipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author', 'description')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
