from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (
    Favorite, Ingredient, Recipe, ShoppingCart, Tag, RecipeIngredient,
    ShoppingCart
)
from .filters import IngredientsFilter, RecipeFilter
from .mixins import RetriveAndListViewSet
from .pagination import ResultsSetPagination
from .permissions import IsAuthorOrAdmin
from .serializers import (
    AddRecipeSerializer, FavoriteSerializer, IngedientSerializer,
    RecipeSerializer, ShoppingCartSerializer, TagSerializer
)
from .utils import download_file_response, get_ingredients_list


class IngredientViewSet(RetriveAndListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngedientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    pagination_class = None


class TagViewSet(RetriveAndListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = ResultsSetPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return AddRecipeSerializer

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.bulk_create([
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient['id'],
                    amount=ingredient['amount']
                )
            ])

    def perform_create(self, serializer):
        author = self.request.user
        image = serializer.validated_data.pop('image')
        ingredients = serializer.validated_data.pop('ingredients')
        recipe = serializer.save(image=image, author=author)
        self.create_ingredients(ingredients, recipe)

    def perform_update(self, serializer):
        data = serializer.validated_data
        ingredients = data.pop('ingredients')
        instance = serializer.save()
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='favorite',
        permission_classes=[IsAuthorOrAdmin],
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Этот рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(favorite,
                                            context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        permission_classes=[IsAuthorOrAdmin],
        methods=['POST', 'DELETE'],
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Этот рецепт уже в корзине покупок!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            shoping_cart = ShoppingCart.objects.create(user=user,
                                                       recipe=recipe)
            serializer = ShoppingCartSerializer(
                shoping_cart, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            delete_shoping_cart = ShoppingCart.objects.filter(user=user,
                                                              recipe=recipe)
            if delete_shoping_cart.exists():
                delete_shoping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        to_buy = get_ingredients_list(request)
        return download_file_response(
            to_buy, settings.INGREDIENTS_LIST_FILENAME)
