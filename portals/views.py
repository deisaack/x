from django.shortcuts import render, redirect
from portals.forms import (
    RegistrationForm,
    EditProfileForm,
)
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import  login_required

def home(request):
    numbers = [1,2,3,4,5]
    name ='De Isaac'

    args = {
        'myName': name,
        'numbers': numbers
    }
    return render(request, 'portals/home.html', args)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return  redirect(reverse('portals:home'))

    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'portals/reg_form.html', args)

def view_profile(request):
    args = {"user": request.user}
    return render(request, 'portals/profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('portals:view_profile'))

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'portals/edit_profile.html', args)


# @login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('portals:view_profile'))
        else:
            return request(reverse('portals:change_password'))

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'portals/change_password.html', args)

