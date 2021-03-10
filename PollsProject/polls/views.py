from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'polls/home.html')

def polls(request):
    return render(request, 'polls/polls.html')

def pollDetail(request, pk):
    context = {'pk': pk}
    return render(request, 'polls/poll-detail.html', context)