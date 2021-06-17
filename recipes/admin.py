from django.contrib import admin

from .models import EatingTimes, Ingredient, Recipe, RecipeIngredient


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    search_fields = ('name',)


class RecipeIngredientAdminInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    inlines = (RecipeIngredientAdminInline,)
    list_display = ('title', 'pub_date', 'author', 'description')
    list_filter = ('pub_date',)
    search_fields = ('title', 'author', 'description')


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


class EatingTimesAdmin(admin.ModelAdmin):
    model = EatingTimes
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(EatingTimes, EatingTimesAdmin)
