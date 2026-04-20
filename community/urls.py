from django.urls import path, include

from community.views import TrailNoteUpdateView, TrailNoteDeleteView

app_name = 'community'
urlpatterns = [
    path('<int:pk>/', include([
        path('edit/', TrailNoteUpdateView.as_view(), name='note_edit'),
        path('delete/', TrailNoteDeleteView.as_view(), name='note_delete'),
    ]))
]