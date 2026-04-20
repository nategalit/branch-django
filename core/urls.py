from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('resources/', views.resource_finder, name='resource_finder'),  # ← add this
]