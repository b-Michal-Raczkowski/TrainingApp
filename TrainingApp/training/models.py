from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Achievement(models.Model):
    date_achieved = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

class Workout(models.Model):
    title = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    duration = models.IntegerField()
    steps = models.TextField()
    is_admin = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    achievement = models.ManyToManyField(Achievement, blank=True)

    def __str__(self):
        return self.title

class UserWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos', default='default.jpg')

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    def __str__(self):
        return self.user.username

    models.signals.post_save.connect(create_user_profile, sender=User)