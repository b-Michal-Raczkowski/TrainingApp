from .models import Achievement

def award_achievement(user, title, description, count=None):
    achievement, created = Achievement.objects.get_or_create(
        user=user,
        title=title,
        defaults={
            'description': description,
            'count': count,
            'collected': True
        }
    )
    if not created and not achievement.collected:
        achievement.collected = True
        achievement.save()
