from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class CodeSnippet(models.Model):
    """Code snippet submitted for review"""
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('csharp', 'C#'),
        ('cpp', 'C++'),
        ('ruby', 'Ruby'),
        ('go', 'Go'),
        ('rust', 'Rust'),
        ('php', 'PHP'),
        ('swift', 'Swift'),
        ('kotlin', 'Kotlin'),
        ('typescript', 'TypeScript'),
        ('sql', 'SQL'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('archived', 'Archived'),
    ]
    
    # Basic info
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="What does this code do? What are you looking for feedback on?")
    code = models.TextField(help_text="Paste your code here")
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    
    # Metadata
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_snippets')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Stats
    view_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Code Snippet"
        verbose_name_plural = "Code Snippets"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.language}) by {self.author.username}"
    
    def get_absolute_url(self):
        return reverse('snippet_detail', kwargs={'pk': self.pk})
    
    def ai_review_count(self):
        """Count of AI reviews"""
        return self.reviews.filter(reviewer_type='ai').count()
    
    def community_review_count(self):
        """Count of community reviews"""
        return self.reviews.filter(reviewer_type='community').count()


class Review(models.Model):
    """Review of a code snippet (can be from AI or community)"""
    REVIEWER_TYPE_CHOICES = [
        ('ai', 'AI Review'),
        ('community', 'Community Review'),
    ]
    
    REVIEW_CATEGORY_CHOICES = [
        ('general', 'General Feedback'),
        ('security', 'Security'),
        ('performance', 'Performance'),
        ('style', 'Code Style'),
        ('best_practices', 'Best Practices'),
        ('bugs', 'Potential Bugs'),
        ('documentation', 'Documentation'),
    ]
    
    SEVERITY_CHOICES = [
        ('info', 'Info'),
        ('suggestion', 'Suggestion'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]
    
    # Relations
    snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews_given')
    
    # Review details
    reviewer_type = models.CharField(max_length=20, choices=REVIEWER_TYPE_CHOICES)
    category = models.CharField(max_length=30, choices=REVIEW_CATEGORY_CHOICES, default='general')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='info')
    content = models.TextField(help_text="The review feedback")
    
    # Engagement
    helpfulness_score = models.IntegerField(default=0)  # Upvotes - Downvotes
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']
    
    def __str__(self):
        reviewer_name = self.reviewer.username if self.reviewer else "AI"
        return f"Review by {reviewer_name} on '{self.snippet.title}'"


class ReviewVote(models.Model):
    """Track upvotes/downvotes on reviews"""
    VOTE_CHOICES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ]
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_votes')
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Review Vote"
        verbose_name_plural = "Review Votes"
        unique_together = ['review', 'user']  # One vote per user per review
    
    def __str__(self):
        vote_type = "👍" if self.vote == 1 else "👎"
        return f"{vote_type} by {self.user.username} on review #{self.review.id}"
    
    def save(self, *args, **kwargs):
        # Update the review's helpfulness score
        super().save(*args, **kwargs)
        self.review.helpfulness_score = self.review.votes.aggregate(
            models.Sum('vote')
        )['vote__sum'] or 0
        self.review.save()


class Comment(models.Model):
    """Comments on code snippets"""
    snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    
    # Optional: reply to another comment (threaded comments)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on '{self.snippet.title}'"