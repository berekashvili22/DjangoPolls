from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

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