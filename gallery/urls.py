from django.urls import path

from gallery.views import PhotoDeleteView

app_name = 'gallery'
urlpatterns = [
    path('<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete')
]