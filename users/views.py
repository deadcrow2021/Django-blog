from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}, Your account has been created.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    user_form = UserUpdateForm()
    profile_form = ProfileUpdateForm()

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,
                                   instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'u_form':user_form, 'p_form':profile_form}
    return render(request, 'users/profile.html', context)