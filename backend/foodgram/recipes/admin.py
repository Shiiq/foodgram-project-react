from django.contrib import admin
from .models import Ingredient, Tag, Recipe, RecipeIngredients, RecipeTags


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
    )
    search_fields = ('name', 'author')

    def ingredient_list(self, obj):
        return (', '.join([
            ingredient.name for ingredient in obj.ingredient.all()
        ]))

    ingredient_list.short_description = 'ingredients'

    def tag_list(self, obj):
        return (', '.join([
            '#' + tag.name for tag in obj.tag.all()
        ]))

    tag_list.short_description = 'tags'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredients)
admin.site.register(RecipeTags)
