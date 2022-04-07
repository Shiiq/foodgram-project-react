from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MinLengthValidator
from webcolors import CSS3_HEX_TO_NAMES
from .utils import get_upload_path


COLORS = list(
    (k, v.capitalize()) for k, v in CSS3_HEX_TO_NAMES.items()
)


class Ingredient(models.Model):
    """Ингредиент."""
    name = models.CharField(
        max_length=50,
        verbose_name='Наименование ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=50,
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
    При создании тега цвет выбирается из таблицы.
    При записи в БД цвет конвертируется в hex-код.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название тега'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )
    color = models.CharField(
        max_length=7,
        choices=COLORS,
        validators=[
            MinLengthValidator(4)
        ]
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
        blank=True,
        null=True,
        upload_to=get_upload_path,
        verbose_name='Картинка'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Название рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, м.',
        validators=[
            MinValueValidator(1)
        ],
    )
    text = models.TextField(
        blank=True,
        null=True,
        max_length=250,
        verbose_name='Описание'
    )
    # is_favorited = models.BooleanField(
    #     blank=True,
    #     null=True,
    #     default=False
    # )
    #
    # is_in_shopping_cart = models.BooleanField(
    #     blank=True,
    #     null=True,
    #     default=False
    # )
    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='RecipeIngredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='RecipeIngredients',
        verbose_name='Ингредиент'
    )
    value = models.FloatField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(0)
        ]
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient')
        ]

    def __str__(self):
        recipe = self.recipe.name
        ingredient = self.ingredient.name
        value = self.value
        measurement_unit = self.ingredient.measurement_unit
        return f'{recipe}: {ingredient}, {value}{measurement_unit}'


class RecipeTags(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='RecipeTags',
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='RecipeTags',
        verbose_name='Тег'
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_tag')
        ]

    def __str__(self):
        return f'{self.recipe.name} #{self.tag.name}'
