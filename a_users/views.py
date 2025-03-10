from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import EmailForm, ProfileFrom
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from allauth.account.utils import send_email_confirmation

# Create your views here.
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect('account_login')
    profile = request.user.profile
    context = {
        'profile': profile,
    }
    return render(request, 'a_users/profile.html', context)

@login_required
def profile_edit_view(request):
    form = ProfileFrom(instance=request.user.profile)
    
    if request.method == 'POST':
        form = ProfileFrom(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    if request.path == reverse('profile-onboarding'):
        onboarding = True
    else:
        onboarding = False
        
    context = {
        'form': form, 
        'onboarding': onboarding,
    }
        
    return render(request, 'a_users/profile_edit.html', context=context)

@login_required
def profile_settings_view(request):
    return render(request, 'a_users/profile_settings.html')

@login_required
def profile_emailchange(request):
    if request.htmx:
        form = EmailForm(instance=request.user)
        context = {
            'form': form, 
        }
        return render(request, 'partials/email_form.html', context=context)
    
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use!')
                return redirect('profile-settings')
            
            form.save()
            
            # Then signal updates emailAddress and set verified to False
            # and confirmation email is sent
            send_email_confirmation(request, request.user)
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Form not valid')
            return redirect('profile-settings')
            
    return redirect('home')


@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')

@login_required
def profile_delete(request):
    user = request.user # this is a way to know the current user
    if request.method == 'POST':
        logout(request) #
        user.delete()
        messages.success(request, 'Account deleted, so sad')
        return redirect('home')
    return render(request, 'a_users/profile_delete.html')