# Generated by Django 3.2.15 on 2022-09-22 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='recipetag',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Название рецепта'),
        ),
        migrations.AddField(
            model_name='recipetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.tag', verbose_name='Тег'),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ingredient', to='recipes.ingredient', verbose_name='Используемые ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='Ингрединты блюда'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_recipe_in_user_shopping_cart'),
        ),
        migrations.AddConstraint(
            model_name='recipetag',
            constraint=models.UniqueConstraint(fields=('tag', 'recipe'), name='unique_recipe_tag'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_ingredient_in_recipe'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_recipe_in_user_favorite'),
        ),
    ]
