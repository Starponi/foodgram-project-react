from rest_framework.serializers import ValidationError
from rest_framework import mixins, viewsets


class RecipeMixin:
    model_def = None
    serializer_def = None
    ValidationError = None

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if self.model_def.objects.filter(user=user,
                                         recipe__id=recipe_id).exists():
            raise ValidationError('ValidationError')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return self.serializer_def(instance.recipe, context=context).data


class RetriveAndListViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    pass