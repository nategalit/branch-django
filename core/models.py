from django.db import models


class Profile(models.Model):
    ACCOUNT_TYPES = [
        ('Volunteer', 'Volunteer'),
        ('Community Member', 'Community Member'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPES)
    total_points = models.IntegerField(default=0)

    class Meta:
        managed = False        # Django won't touch this table
        db_table = 'users'     # Points at your existing Postgres table

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Location(models.Model):
    SERVICE_TYPES = [
        ('Food Pantry', 'Food Pantry'),
        ('Clothing', 'Clothing'),
        ('Shelter', 'Shelter'),
        ('General Volunteering', 'General Volunteering'),
    ]

    name = models.CharField(max_length=150)
    primary_service = models.CharField(max_length=100, choices=SERVICE_TYPES)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'locations'

    def __str__(self):
        return self.name


class Visit(models.Model):
    VISIT_TYPES = [
        ('Volunteered', 'Volunteered'),
        ('Received Resources', 'Received Resources'),
    ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_column='user_id'   # matches the actual column name in your visits table
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        db_column='location_id'
    )
    visit_type = models.CharField(max_length=50, choices=VISIT_TYPES)
    hours_logged = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    visit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'visits'

    def __str__(self):
        return f"{self.profile} - {self.visit_type} at {self.location}"