from django.contrib import admin
from .models import Waypoint, WaypointCategory



@admin.register(WaypointCategory)
class WaypointCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Waypoint)
class WaypointAdmin(admin.ModelAdmin):
    list_display = ['name', 'trip', 'order', 'latitude', 'longitude']
    list_filter = ['categories']