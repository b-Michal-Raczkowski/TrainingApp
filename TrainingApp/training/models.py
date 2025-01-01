from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Workout(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='workouts')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_workouts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Challenge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    goal = models.CharField(max_length=100)
    reward_points = models.IntegerField()

    def __str__(self):
        return self.title

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    description = models.TextField()
    criteria = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos', default='default.jpg')

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)


    def __str__(self):
        return self.user.username

    models.signals.post_save.connect(create_user_profile, sender=User)

class UserWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_workouts')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='user_workouts')
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout.title}"

class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_challenges')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='user_challenges')
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"