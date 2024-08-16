from django.contrib import admin

from .models import CustomUser, Balance, Subscription

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Balance)
admin.site.register(Subscription)