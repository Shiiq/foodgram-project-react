from django.contrib import admin
from .models import Ingredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name',
        'measurement_unit'
    )



class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name',
        'slug', 'color'
    )
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
