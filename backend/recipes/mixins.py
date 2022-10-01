from rest_framework import mixins, viewsets


class RecipeMixin:
    serializer_def = None

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return self.serializer_def(instance.recipe, context=context).data


class RetriveAndListViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    pass
