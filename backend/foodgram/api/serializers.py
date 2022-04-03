from recipes.models import Ingredient, Tag
from rest_framework import serializers


class IngredientsSerializer(serializers.ModelSerializer):
    """Обслуживает модель Ingredient"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagsSerializer(serializers.ModelSerializer):
    """Обслуживает модель Tag"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
