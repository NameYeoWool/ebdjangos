from django.contrib import admin
from .models import Room, SeatInfo, Event, FoodInfo, Coment

# Register your models here.
admin.site.register(Room)
admin.site.register(SeatInfo)
admin.site.register(Event)
admin.site.register(FoodInfo)
admin.site.register(Coment)