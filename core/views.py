from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db.models import Sum
from .models import Profile, Location, Visit
from .forms import VisitForm, SignupForm

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

def resource_finder(request):
    locations = Location.objects.filter(is_active=True)
    selected_service = request.GET.get('service', 'Show All')
    search_term = request.GET.get('q', '')

    if selected_service and selected_service != 'Show All':
        locations = locations.filter(primary_service=selected_service)
    if search_term:
        locations = locations.filter(name__icontains=search_term)

    services = Location.objects.filter(is_active=True).values_list(
        'primary_service', flat=True).distinct()

    return render(request, 'core/resource_finder.html', {
        'locations': locations.order_by('name'),
        'services': services,
        'selected_service': selected_service,
        'search_term': search_term,
    })

def log_activity(request):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save()
            if visit.visit_type == 'Volunteered':
                points = int(visit.hours_logged * 100)
                visit.profile.total_points += points
                visit.profile.save()
                messages.success(request,
                    f"🎉 Logged {visit.hours_logged} hours and earned {points} points!")
            else:
                messages.success(request,
                    "✅ Check-in successful. We're glad we could help today!")
            return redirect('log_activity')
    else:
        form = VisitForm()

    return render(request, 'core/log_activity.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create the Django auth User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            # Create the linked Profile
            Profile.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                account_type=form.cleaned_data['account_type'],
            )
            # Log them in automatically
            login(request, user)
            messages.success(request, f"Welcome to Branch, {user.first_name}! 🌿")
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})