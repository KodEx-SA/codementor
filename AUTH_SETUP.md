# Adding Authentication to CodeMentor

## Files to Update/Create

You need to replace/create these files in your project:

### 1. **users/forms.py**
- Download: `users_forms.py`
- Save as: `users/forms.py`
- This creates registration and profile update forms

### 2. **users/views.py**
- Download: `users_views.py`
- Save as: `users/views.py`
- This handles registration, login, profile, and dashboard

### 3. **users/urls.py**
- Download: `users_urls.py`
- Save as: `users/urls.py`
- This defines URL patterns for authentication

### 4. **Update Main URLs (codementor/urls.py)**
Add this import at the top:
```python
from django.urls import path, include  # Add 'include'
```

Then add this to urlpatterns:
```python
path('users/', include('users.urls')),
```

Full example:
```python
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/', include('users.urls')),  # Add this line
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 5. **Create Template Directories**
```bash
mkdir -p templates/users
```

### 6. **Templates to Create**
- `users_register.html` → Save as: `templates/users/register.html`
- `users_login.html` → Save as: `templates/users/login.html`
- `users_profile.html` → Save as: `templates/users/profile.html`

### 7. **Update Existing Templates**
- `base_updated.html` → Replace: `templates/base.html`
- `home_updated.html` → Replace: `templates/home.html`

## Step-by-Step Installation

```bash
# 1. Stop Docker containers
sudo docker-compose down

# 2. Create the users templates directory
mkdir -p templates/users

# 3. Copy all the downloaded files to their correct locations
# (use your file manager or cp commands)

# 4. Update codementor/urls.py as shown above

# 5. Rebuild and start containers
sudo docker-compose up --build -d

# 6. Wait for services to start
sleep 5

# 7. Test it out!
# Go to: http://localhost:8000
```

## Testing the Features

### Test Registration:
1. Go to http://localhost:8000/users/register/
2. Create a new account
3. You should be logged in automatically

### Test Login:
1. Logout
2. Go to http://localhost:8000/users/login/
3. Login with your credentials

### Test Profile:
1. Click "Profile" in the navigation
2. Update your bio and preferred languages
3. Save changes

## Troubleshooting

If you get errors:
```bash
# Check logs
sudo docker-compose logs web

# Restart web container
sudo docker-compose restart web
```

If templates aren't found:
```bash
# Make sure templates directory structure is correct
ls -la templates/
ls -la templates/users/
```

## What's Next?

After authentication works, we'll build:
1. Code submission form
2. AI review integration with Claude API
3. Display reviews and comments
4. Voting system

Let me know when authentication is working!