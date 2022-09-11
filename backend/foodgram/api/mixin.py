from rest_framework.serializers import ValidationError


class MyMixin:
    model_def = None
    serializer_def = None
    text_error = None

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if self.model.objects.filter(user=user, recipe__id=recipe_id).exists():
            raise ValidationError("text_error")
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return self.serializer(instance.recipe, context=context).data


# class MyMixin:
#     serializer = None

#     def to_representation(self, instance):
#         request = self.context.get('request')
#         context = {'request': request}
#         return self.serializer(instance.recipe, context=context).data


# class MyMixin:
#     def to_representation(self, **kwargs):
#         instance = kwargs
#         request = self.context.get('request')
#         context = {'request': request}
#         to_context = ShortRecipeSerializer(
#             instance.recipe, context=context).data
#         return to_context
