from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Ingredient, Recipe, RecipeFavorite, RecipeIngredients,
                     RecipeTags, ShoppingCart, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'measurement_unit'
    )
    search_fields = ('name', )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'slug', 'color'
    )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'author', 'ingredient_list',
        'tag_list', 'image_preview', 'is_favorited_count'
    )
    list_filter = ('author', 'name', 'tags')
    search_fields = ('author', 'name')
    readonly_fields = ('image_preview', )

    def is_favorited_count(self, obj):
        """Сколько раз добавлен в избранное."""

        return obj.recipe_favorite.count()

    def ingredient_list(self, obj):
        """Показ ингредиентов в рецепте."""

        return (', '.join([
            ingredient.name for ingredient in obj.ingredients.all()
        ]))

    def tag_list(self, obj):
        """Показ тегов рецепта."""

        return (', '.join([
            '#' + tag.name for tag in obj.tags.all()
        ]))

    def image_preview(self, obj):
        """Превью картинки рецепта."""

        if not obj.image:
            return ''
        return mark_safe(
            f'<img src="{obj.image.url}" '
            f'alt="{obj.name}" '
            f'width="250px" '
        )

    is_favorited_count.short_description = 'Добавили в избранное раз'
    ingredient_list.short_description = 'Ингредиенты'
    tag_list.short_description = 'Теги'
    image_preview.short_description = 'Картинка'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredients)
admin.site.register(RecipeTags)
admin.site.register(RecipeFavorite)
admin.site.register(ShoppingCart)
