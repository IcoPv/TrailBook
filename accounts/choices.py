from django.db.models import TextChoices


class VehicleType(TextChoices):
    MOTORCYCLE = 'motorcycle', 'Motorcycle'
    FOURXFOUR = '4x4', '4x4 / Overland Vehicle'
    BICYCLE = 'bicycle', 'Bicycle'
    OTHER = 'other', 'Other'


class ExperienceLevel(TextChoices):
    BEGINNER = 'beginner', 'Beginner'
    INTERMEDIATE = 'intermediate', 'Intermediate'
    ADVANCED = 'advanced', 'Advanced'
    EXPERT = 'expert', 'Expert'
