from django.shortcuts import render
from django.db.models import Sum
from .models import Profile, Location, Visit


def dashboard(request):
    total_volunteers = Profile.objects.filter(account_type='Volunteer').count()
    total_members = Profile.objects.filter(account_type='Community Member').count()
    total_hours = Visit.objects.filter(visit_type='Volunteered').aggregate(
        Sum('hours_logged'))['hours_logged__sum'] or 0
    active_locations = Location.objects.filter(is_active=True).count()
    recent_visits = Visit.objects.select_related(
        'profile', 'location').order_by('-visit_date')[:10]

    return render(request, 'core/dashboard.html', {
        'total_volunteers': total_volunteers,
        'total_members': total_members,
        'total_hours': round(total_hours, 1),
        'active_locations': active_locations,
        'recent_visits': recent_visits,
    })