from django.contrib import admin
from .models import Profile, Location, Visit


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'account_type', 'total_points')
    list_filter = ('account_type',)
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_service', 'address', 'is_active')
    list_filter = ('primary_service', 'is_active')
    search_fields = ('name', 'address')


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('profile', 'location', 'visit_type', 'hours_logged', 'visit_date')
    list_filter = ('visit_type',)