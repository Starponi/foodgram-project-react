from django.contrib.auth import get_user_model
# from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
# from rest_framework.serializers import ValidationError

from recipes.models import (
    RecipeIngredient, Favorite, Ingredient, Recipe, ShoppingCart, Tag, 
)
from users.serializers import CustomUserSerializer

from .mixins import RecipeMixin

User = get_user_model()


class IngedientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='ingredient'
    )
    name = serializers.SlugRelatedField(
        source='ingredient',
        read_only=True,
        slug_field='name'
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient',
        read_only=True,
        slug_field='measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj,
                                       user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj,
                                           user=request.user).exists()


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class AddRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    ingredients = AddIngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    cooking_time = serializers.IntegerField()

    def validate_ingredients(self, value):
        ingredients_set = []
        for ingredient in value:
            if ingredient['id'] in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторяться!'
                )
            elif ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    'Колличество ингредиентов должно быть положительным!'
                )
            else:
                ingredients_set.append(ingredient['id'])
        return value

    def validate_tags(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                'Тег должен быть уникальным!'
            )
        return value

    def validate_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Время готовки не может быть 0!'
            )
        return value

    def to_representation(self, recipe):
        data = ShortRecipeSerializer(
            recipe, context={'request': self.context.get('request')}).data
        return data
    
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name',
                  'image', 'text', 'cooking_time')


class FavoriteSerializer(RecipeMixin, serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    model_def = Favorite
    serializer_def = ShortRecipeSerializer
    ValidationError = 'Рецепт уже добавлен!'

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class ShoppingCartSerializer(RecipeMixin, serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    model_def = ShoppingCart
    serializer_def = ShortRecipeSerializer
    ValidationError = 'Рецепт уже добавлен в список покупок!'

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
