from django.urls import path
from . import views
from . import forms

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('resources/', views.resource_finder, name='resource_finder'),
    path('log/', views.log_activity, name='log_activity'),
    path('signup/', views.signup, name='signup'),  # ← add this
]