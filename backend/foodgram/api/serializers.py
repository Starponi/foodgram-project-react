from django.contrib.auth import get_user_model
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from recipes.models import (
    AmountIngredient, Favorite, Ingredient, Recipe, ShoppingCart, Tag
)
from users.serializers import CustomUserSerializer

from .mixin import MyMixin

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
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True)
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
        ingredients = AmountIngredient.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj,
                                           user=request.user).exists()


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = AmountIngredient
        fields = ('id', 'amount')


class AddRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    ingredients = AddIngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name',
                  'image', 'text', 'cooking_time')

    def __validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise ValidationError(
                'Колличество ингредиентов должно быть положительным!')
        ingredients_count = len(ingredients)
        ingredients_set = len(set([i['id'] for i in ingredients]))
        if ingredients_count > ingredients_set:
            raise ValidationError('Ингредиенты не должны повторяться!')
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise ValidationError('Время готовки не может быть 0')
        return data

    def __add_recipe_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            if (AmountIngredient.objects.
               filter(recipe=recipe, ingredient=ingredient_id).exists()):
                amount += F('amount')
            objs = [AmountIngredient(
                recipe=recipe,
                ngredient=ingredient_id,
                defaults={'amount': amount},
            )
            ]
            AmountIngredient.objects.bulk_create(objs)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_recipe_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        recipe.name = validated_data.get('name', 'recipe.name')
        recipe.text = validated_data.get('text', 'recipe.text')
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time)
        recipe.image = validated_data.get('image', recipe.image)
        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients')
            recipe.ingredients.clear()
            self.add_recipe_ingredients(ingredients, recipe)
        if 'tags' in self.initial_data:
            tags_data = validated_data.pop('tags')
            recipe.tags.set(tags_data)
        recipe.save()
        return recipe

    def representation(self, recipe):
        data = ShortRecipeSerializer(
            recipe, context={'request': self.context.get('request')}).data
        return data


class FavoriteSerializer(MyMixin, serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    model_def = Favorite
    serializer_def = ShortRecipeSerializer
    text_error = 'Рецепт уже добавлен!'

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class ShoppingCartSerializer(MyMixin, serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    model_def = ShoppingCart
    serializer_def = ShortRecipeSerializer
    text_error = 'Рецепт уже добавлен в список покупок!'

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
