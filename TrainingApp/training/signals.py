from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Workout
from .utils import award_achievement




@receiver(post_save, sender=Workout)
def award_first_workout_achievement(sender, instance, created, **kwargs):
    if created:
        user = instance.created_by  # Ensure this is the correct user instance
        award_achievement(user, "Create your first workout", "Awarded for creating your first workout.", 1)
        award_achievement(user, "Create 5 workouts", "Awarded for creating 5 workouts.", 5)
        award_achievement(user, "Create 10 workouts", "Awarded for creating 10 workouts.", 10)