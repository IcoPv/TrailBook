from django.db.models import TextChoices


class Difficulty(TextChoices):
    EASY = 'easy', 'Easy'
    MODERATE = 'moderate', 'Moderate'
    CHALLENGING = 'challenging', 'Challenging'
    EXTREME = 'extreme', 'Extreme'


class VehicleTypeTrips(TextChoices):
    MOTORCYCLE = 'motorcycle', 'Motorcycle'
    FOURXFOUR = '4x4', '4x4 / Overland Vehicle'
    BICYCLE = 'bicycle', 'Bicycle'
    MIXED = 'mixed', 'Mixed'
    OTHER = 'other', 'Other'