from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['trip', 'uploaded_by', 'uploaded_at', 'is_thumbnail_generated']
    list_filter = ['is_thumbnail_generated', 'uploaded_at']