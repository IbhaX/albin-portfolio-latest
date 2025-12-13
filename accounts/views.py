from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('pages:home')


def register(request):
    if request.user.is_authenticated:
        return redirect('pages:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_member = True  # Auto-grant membership on registration
            user.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('pages:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})
