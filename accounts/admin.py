from django.contrib import admin

from .models import FriendShip, Profile, User

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(FriendShip)
# Register your models here.
