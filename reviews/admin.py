from django.contrib import admin
from .models import CodeSnippet, Review, ReviewVote, Comment


@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'author', 'status', 'view_count', 'created_at']
    list_filter = ['language', 'status', 'created_at']
    search_fields = ['title', 'description', 'code', 'author__username']
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'language', 'author')
        }),
        ('Code', {
            'fields': ('code',)
        }),
        ('Status & Stats', {
            'fields': ('status', 'view_count')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        # Make author readonly after creation
        if obj:
            return self.readonly_fields + ['author']
        return self.readonly_fields


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['snippet', 'reviewer_type', 'category', 'severity', 'helpfulness_score', 'created_at']
    list_filter = ['reviewer_type', 'category', 'severity', 'created_at']
    search_fields = ['content', 'snippet__title', 'reviewer__username']
    readonly_fields = ['helpfulness_score', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Review Details', {
            'fields': ('snippet', 'reviewer', 'reviewer_type')
        }),
        ('Classification', {
            'fields': ('category', 'severity')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Engagement', {
            'fields': ('helpfulness_score',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'vote', 'created_at']
    list_filter = ['vote', 'created_at']
    search_fields = ['review__snippet__title', 'user__username']
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['snippet', 'author', 'parent', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username', 'snippet__title']
    date_hierarchy = 'created_at'
    raw_id_fields = ['snippet', 'parent']