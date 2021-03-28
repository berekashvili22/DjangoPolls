from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from users.forms import UserUpdateForm
from django.contrib import messages

def home(request):
    return render(request, 'polls/home.html')

def about(request):
    return render(request, 'polls/about.html')

def poll(reqeust):
    return render(reqeust, 'polls/poll.html')

def polls(request):
    return render(request, 'polls/polls.html')

@login_required(login_url='login')
def pollDetail(request, pk):
    context = {'pk': pk}
    return render(request, 'polls/poll-detail.html', context)

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user, user=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your profile has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'form': u_form,
    }
    return render(request, 'polls/profile.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated.')
            return redirect('login')

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'polls/change_password.html', {
        'form': form
    })