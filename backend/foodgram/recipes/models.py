import re

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator


class Ingridient(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Ингридиент'
    )
    measurement_unit = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}'


class IngridientQuantity(models.Model):
    ingridient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
        related_name='ingridient',
        verbose_name='Ингридиент'
    )
    value = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'

    def __str__(self):
        name = self.ingridient.name
        value = self.value
        measurement_unit = self.ingridient.measurement_unit
        return f'{name} - {value} {measurement_unit}'


# class Tag(models.Model):
#     name = models.CharField(
#         max_length=50,
#         unique=True,
#         verbose_name='Тег'
#     )
#     slug = models.SlugField(
#         max_length=50,
#         unique=True
#     )
#     # color = models.CharField(
#     #     max_length=7
#     # )
#
#     class Meta:
#         ordering = ['name']
#         verbose_name = 'Тег'
#         verbose_name_plural = 'Теги'
#
#
# class Recipe(models.Model):
#     # author =
#     # ingridient = models.ManyToManyField()
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
# class RecipeIngridient(models.Model):
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='recipe'
#     )
#     ingridient = models.ForeignKey(
#         Ingridient,
#         on_delete=models.CASCADE,
#         related_name='ingridient'
#     )
