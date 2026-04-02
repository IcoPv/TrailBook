from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from . import views

app_name = 'accounts'

profile_patterns = [
    path('edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('delete/', views.ProfileDeleteView.as_view(), name='profile_delete'),
    path('<str:username>/', views.ProfileDetailView.as_view(), name='profile'),
]

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', include(profile_patterns)),
]