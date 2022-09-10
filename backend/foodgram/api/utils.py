from django.db.models import Sum
from django.http.response import HttpResponse

from recipes.models import AmountIngredient

from .serializers import ShortRecipeSerializer


def get_ingredients_list(request):
    ingredients = AmountIngredient.objects.filter(
        recipe__carts__user=request.user.id).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    to_buy = []
    for position, ingredient in enumerate(ingredients, start=1):
        to_buy.append(
            f'\n{position}. {ingredient["ingredient__name"]}:'
            f' {ingredient["amount"]}'
            f'({ingredient["ingredient__measurement_unit"]})'
        )
    response = HttpResponse(to_buy, content_type='text')
    response['Content-Disposition'] = (
        'attachment;filename=shopping_cart.pdf'
    )
    return response


def download_file_response(list_to_download, filename):
    response = HttpResponse(list_to_download, 'Content-Type: text/plain')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return


def to_representation(self, instance):
    request = self.context.get('request')
    context = {'request': request}
    return ShortRecipeSerializer(instance.recipe, context=context).data
