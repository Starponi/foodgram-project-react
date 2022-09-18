from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .filters import IngredientsFilter, RecipeFilter
from .pagination import ResultsSetPagination
from .permissions import IsAuthorOrAdmin
from .serializers import (
    AddRecipeSerializer, FavoriteSerializer, IngedientSerializer,
    RecipeSerializer, ShoppingCartSerializer, TagSerializer
)
from .utils import download_file_response, get_ingredients_list


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngedientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = ResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return AddRecipeSerializer

    @staticmethod
    def __post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def __delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(permission_classes=[IsAuthorOrAdmin], detail=True)
    def favorite(self, request, pk):
        return self.__post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.__delete_method_for_actions(
            request=request, pk=pk, model=Favorite)

    @action(detail=True, permission_classes=[IsAuthorOrAdmin])
    def shopping_cart(self, request, pk):
        return self.__post_method_for_actions(
            request=request, pk=pk, serializers=ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.__delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        to_buy = get_ingredients_list(request)
        return download_file_response(
            to_buy, settings.INGREDIENTS_LIST_FILENAME)
