from django.contrib import admin
from .models import Amenity, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass
