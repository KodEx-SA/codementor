from django.contrib import admin
from .models import UserProfile, Badge, UserBadge, SkillProgress


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'reputation_points', 'level', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'bio', 'avatar')
        }),
        ('Gamification', {
            'fields': ('reputation_points', 'level')
        }),
        ('Preferences', {
            'fields': ('preferred_languages',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'points_required', 'created_at']
    list_filter = ['badge_type']
    search_fields = ['name', 'description']
    ordering = ['points_required']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge', 'earned_at']
    search_fields = ['user__username', 'badge__name']
    date_hierarchy = 'earned_at'


@admin.register(SkillProgress)
class SkillProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill_area', 'level', 'experience_points', 'updated_at']
    list_filter = ['skill_area', 'level']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['user', 'skill_area']