from django.contrib import admin

from .models import Like, Tweet

# Register your models here.
admin.site.register(Tweet)
admin.site.register(Like)
