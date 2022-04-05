from django.contrib import admin
from .models import Ingredient, Tag, Recipe, RecipeIngredients, RecipeTags
from django.utils.safestring import mark_safe


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name',
        'measurement_unit'
    )
    search_fields = ('name', )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name',
        'slug', 'color'
    )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name',
        'author', 'cooking_time',
        'ingredient_list', 'tag_list',
        'image_preview'
    )
    search_fields = ('name', 'author')
    readonly_fields = ('image_preview', )

    def ingredient_list(self, obj):
        return (', '.join([
            ingredient.name for ingredient in obj.ingredient.all()
        ]))

    def tag_list(self, obj):
        return (', '.join([
            '#' + tag.name for tag in obj.tag.all()
        ]))

    def image_preview(self, obj):
        if not obj.image:
            return ''
        return mark_safe(
            f'<img src="{obj.image.url}" '
            f'alt="{obj.name}" '
            f'width="250px" '
        )

    ingredient_list.short_description = 'Ингредиенты'
    tag_list.short_description = 'Теги'
    image_preview.short_description = 'Картинка'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredients)
admin.site.register(RecipeTags)
