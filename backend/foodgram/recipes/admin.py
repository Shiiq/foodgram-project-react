from django.contrib import admin

from .models import Ingridient, IngridientQuantity
from django.db.models import Sum

class IngridientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
        'get_total_value'
    )

    def get_total_value(self, obj):
        q = obj.ingridient.all().aggregate(Sum('value'))
        return q['value__sum']

    get_total_value.short_description = 'Общее количество'

# class IngridientQuantityAdmin(admin.ModelAdmin):
#     list_display = (
#         'pk',
#         'ingridient',
#         'value'
#     )


admin.site.register(Ingridient, IngridientAdmin)
admin.site.register(IngridientQuantity)
# admin.site.register(IngridientQuantity, IngridientQuantityAdmin)
