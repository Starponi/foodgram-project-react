from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        max_length=20,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=20,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=50,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipe_images/',
    )
    text = models.TextField(
        verbose_name='Описание блюда',
        help_text='Добавьте описание блюда',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингрединты блюда',
        through='AmountIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        default=0,
        validators=(
            MinValueValidator(
                1, 'Время должно быть хотя бы 1 минута!'
            ),
            MaxValueValidator(
                600, 'Слишком большое время приготовления!'
            ),
        ),
    )
    pud_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id', )

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Используемые ингредиенты',
        related_name='ingredient',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,

    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        default=0,
        validators=(
            MinValueValidator(
                0.1, 'Нужно несколько ингредиентов!'
            ),
            MaxValueValidator(
                600, 'Слишком много!'
            ),
        ),
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient', ),
                name='unique_ingredient_in_recipe'
            ),
        )

    def __str___(self):
        return f'{self.ingredient} {self.recipe}'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тег')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = (
            models.UniqueConstraint(
                fields=('tag', 'recipe', ),
                name='unique_recipe_tag'
            ),
        )

    def __str___(self):
        return f'{self.tag} {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('-id', )
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe', ),
                name='unique_recipe_in_user_favorite'
            ),
        )

    def __str___(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт в спитке покупок'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ('-id', )
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe', ),
                name='unique_recipe_in_user_shopping_cart'
            ),
        )

    def __str___(self):
        return f'{self.user} {self.recipe}'
