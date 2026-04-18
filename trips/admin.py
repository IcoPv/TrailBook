from django.contrib import admin

from trips.models import Tag, Trip


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'difficulty', 'created_at']
    list_filter = ['difficulty', 'vehicle_type']
