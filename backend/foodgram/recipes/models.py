from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MinLengthValidator
from webcolors import CSS3_HEX_TO_NAMES

COLORS = list(
    (k, v.capitalize()) for k, v in CSS3_HEX_TO_NAMES.items()
)


class Ingredient(models.Model):
    """Ингредиент:наименование и единица измерения"""
    name = models.CharField(
        max_length=50,
        verbose_name='Ингредиент'
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
        verbose_name='Тег'
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


# class IngredientQuantity(models.Model):
#     ingredient = models.ForeignKey(
#         Ingredient,
#         on_delete=models.CASCADE,
#         related_name='ingredient',
#         verbose_name='Ингредиент'
#     )
#     value = models.PositiveIntegerField(
#         verbose_name='Количество',
#         validators=[MinValueValidator(1)],
#     )
#
#     class Meta:
#         verbose_name = 'Количество ингредиента'
#         verbose_name_plural = 'Количество ингредиентов'
#
#     def __str__(self):
#         name = self.ingredient.name
#         value = self.value
#         measurement_unit = self.ingredient.measurement_unit
#         return f'{name} - {value} {measurement_unit}'
# class Recipe(models.Model):
#     # author =
#     # ingredient = models.ManyToManyField()
#     # tag = models.ManyToManyField()
#     image = models.ImageField(
#         verbose_name='Картинка',
#         upload_to='recipes/'
#     )
#     name = models.CharField(
#         max_length=50
#     )
#     cooking_time = models.PositiveSmallIntegerField(
#         validators=[MinValueValidator(1)],
#     )
#     description = models.TextField()
#
#     class Meta:
#         ordering = ['-id']
#         verbose_name = 'Рецепт'
#         verbose_name_plural = 'Рецепты'
#
#
# class RecipeTag(models.Model):
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='recipe'
#     )
#     tag = models.ForeignKey(
#         Tag,
#         on_delete=models.CASCADE,
#         related_name='tag'
#     )
#
# class RecipeIngredient(models.Model):
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='recipe'
#     )
#     ingredient = models.ForeignKey(
#         Ingredient,
#         on_delete=models.CASCADE,
#         related_name='ingredient'
#     )
