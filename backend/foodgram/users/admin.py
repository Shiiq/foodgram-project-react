from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subscription


# class SubscribeAdmin(admin.ModelAdmin):
#     list_display = (
#         'author', 'subscriber'
#     )


admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
