from django.conf import settings
from django.core.validators import (MaxLengthValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models
from webcolors import CSS3_HEX_TO_NAMES

from .querysets import RecipeManager
from .utils import get_upload_path

COLORS = list(
    (k, v.capitalize()) for k, v in CSS3_HEX_TO_NAMES.items()
)


class Ingredient(models.Model):
    """Ингредиент."""

    name = models.CharField(
        max_length=255,
        verbose_name='Ингредиент'
    )
    measurement_unit = models.CharField(
        max_length=255,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """
    Тег.
    При создании тега в админке цвет выбирается
    из импортированной таблицы библиотеки webcolors.
    При записи в БД цвет конвертируется в hex-код.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название тега'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True
    )
    color = models.CharField(
        max_length=7,
        choices=COLORS,
        validators=[MinLengthValidator(4), MaxLengthValidator(7)]
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепт."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTags',
        related_name='recipes',
        verbose_name='Тег'
    )
    image = models.ImageField(
        default=None,
        upload_to=get_upload_path,
        verbose_name='Картинка'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, м.',
        validators=[MinValueValidator(1)]
    )
    text = models.TextField(
        default='Введите текст',
        max_length=255,
        verbose_name='Описание'
    )
    objects = RecipeManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    """Связка рецепт-ингредиент-количество."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент'
    )
    amount = models.FloatField(
        verbose_name='Количество',
        validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_for_recipe'
            )
        ]

    def __str__(self):
        recipe = self.recipe
        ingredient = self.ingredient.name
        amount = self.amount
        return f'{recipe}: {ingredient}, {amount}'


class RecipeTags(models.Model):
    """Связка рецепт-тег."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tags',
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipe_tags',
        verbose_name='Тег'
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_tag_for_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} #{self.tag}'


class RecipeFavorite(models.Model):
    """Избранные рецепты. Связка рецепт-пользователь."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_favorite',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipe_favorite',
        verbose_name='Пользователь'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_in_favorite'
            )
        ]

    def __str__(self):
        user = self.user
        recipe = self.recipe
        return f'{user} добавил "{recipe}" в избранное'


class ShoppingCart(models.Model):
    """Рецепты для списка покупок. Связка рецепт-пользователь."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_cart',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Корзина для покупок'
        verbose_name_plural = 'Корзина для покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_in_shopping_cart'
            )
        ]

    def __str__(self):
        user = self.user
        recipe = self.recipe
        return f'{user} добавил "{recipe}" в корзину'
