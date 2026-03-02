from django.contrib import admin
from .models import Room, Player, Image, RoomHitTarget

# Register your models here.
admin.site.register(Room)
admin.site.register(Player)
admin.site.register(Image)
admin.site.register(RoomHitTarget)
