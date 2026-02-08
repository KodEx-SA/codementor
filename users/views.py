from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, UserUpdateForm, UserProfileUpdateForm
from .models import UserProfile, Badge, UserBadge


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to CodeMentor, {user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.profile)
    
    # Get user's badges
    user_badges = UserBadge.objects.filter(user=request.user).select_related('badge')
    
    # Get user's code snippets count
    snippets_count = request.user.code_snippets.count()
    reviews_given_count = request.user.reviews_given.count()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_badges': user_badges,
        'snippets_count': snippets_count,
        'reviews_given_count': reviews_given_count,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def dashboard(request):
    """User dashboard view"""
    # Get user's recent code snippets
    recent_snippets = request.user.code_snippets.all()[:5]
    
    # Get user's skill progress
    skill_progress = request.user.skill_progress.all()
    
    # Get available badges
    all_badges = Badge.objects.all()
    earned_badge_ids = request.user.badges.values_list('badge_id', flat=True)
    
    context = {
        'recent_snippets': recent_snippets,
        'skill_progress': skill_progress,
        'all_badges': all_badges,
        'earned_badge_ids': earned_badge_ids,
    }
    
    return render(request, 'users/dashboard.html', context)