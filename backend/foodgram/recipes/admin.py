from django.contrib import admin

from .models import (AmountIngredient, Favorite, Ingredient, Recipe, RecipeTag,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientRecipeInline(admin.TabularInline):
    model = AmountIngredient
    min_num = 1
    extra = 1


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    min_num = 1
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'get_favorites_count')
    list_filter = ('name', 'author', 'tags',)
    inlines = (IngredientRecipeInline, RecipeTagInline)

    def get_favorites_count(self, obj):
        return obj.get_favorites_count.all().count()

    get_favorites_count.short_description = (
        'Количество избранных пользователей')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
