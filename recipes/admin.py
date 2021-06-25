from django.contrib import admin

from .models import (Basket, EatingTimes, Favorite, Ingredient,
                     Recipe, RecipeIngredient, Subscription)


class BasketAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user',)


class EatingTimesAdmin(admin.ModelAdmin):
    model = EatingTimes
    prepopulated_fields = {'slug': ('title',)}


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    list_filter = ('name',)
    search_fields = ('name',)


class RecipeIngredientAdminInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    inlines = (RecipeIngredientAdminInline,)
    list_display = ('title', 'pub_date', 'author', 'description')
    list_filter = ('title', 'pub_date',)
    search_fields = ('title', 'author', 'description')


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('author', 'user',)


admin.site.register(Basket, BasketAdmin)
admin.site.register(EatingTimes, EatingTimesAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
