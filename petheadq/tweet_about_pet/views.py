from django.shortcuts import render
from .models import Tweet
from .forms import TweetFrom, UserRegistraionFrom
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetFrom(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetFrom()
    return render(request, 'tweet_form.html', {'form': form})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == 'POST':
        form = TweetFrom(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetFrom(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    # Fetch the tweet object or return a 404 error if not found
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    
    # Check if the request is a POST request (indicating form submission)
    if request.method == 'POST':
        tweet.delete()  # Delete the tweet
        return redirect('tweet_list')  # Redirect to the tweet list page after deletion

    # Render the confirmation template
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

def register(request):
    if request.method =='POST':
        form = UserRegistraionFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistraionFrom()
    return render(request, 'registration/register.html', {'form': form})