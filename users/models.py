from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile with gamification features"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Gamification
    reputation_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    
    # Preferences
    preferred_languages = models.CharField(max_length=200, blank=True, help_text="Comma-separated list of programming languages")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def add_points(self, points):
        """Add reputation points and potentially level up"""
        self.reputation_points += points
        # Level up every 100 points
        new_level = (self.reputation_points // 100) + 1
        if new_level > self.level:
            self.level = new_level
        self.save()


class Badge(models.Model):
    """Achievements and badges users can earn"""
    BADGE_TYPES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES, default='bronze')
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji or icon class")
    points_required = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badges"
        ordering = ['points_required']
    
    def __str__(self):
        return f"{self.name} ({self.get_badge_type_display()})"


class UserBadge(models.Model):
    """Track which badges users have earned"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "User Badge"
        verbose_name_plural = "User Badges"
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class SkillProgress(models.Model):
    """Track user's progress in specific skill areas"""
    SKILL_AREAS = [
        ('python_basics', 'Python Basics'),
        ('python_advanced', 'Python Advanced'),
        ('javascript_basics', 'JavaScript Basics'),
        ('javascript_advanced', 'JavaScript Advanced'),
        ('security', 'Security Best Practices'),
        ('performance', 'Performance Optimization'),
        ('code_style', 'Code Style & Readability'),
        ('testing', 'Testing & Quality'),
        ('algorithms', 'Algorithms & Data Structures'),
        ('databases', 'Database Design'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_progress')
    skill_area = models.CharField(max_length=50, choices=SKILL_AREAS)
    level = models.IntegerField(default=1)
    experience_points = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Skill Progress"
        verbose_name_plural = "Skill Progress"
        unique_together = ['user', 'skill_area']
        ordering = ['user', 'skill_area']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_skill_area_display()} (Level {self.level})"
    
    def add_experience(self, points):
        """Add experience points and level up if needed"""
        self.experience_points += points
        # Level up every 50 XP
        new_level = (self.experience_points // 50) + 1
        if new_level > self.level:
            self.level = new_level
        self.save()


# Signal to automatically create UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()