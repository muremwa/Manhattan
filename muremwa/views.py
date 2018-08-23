from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from blog.models import Comment, Post


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form':form})


# check if a user name exists
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__icontains=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = '{} already exists'.format(username)
    return JsonResponse(data)


# profile page
@login_required
def profile(request):
    comments = Comment.objects.filter(user=request.user.profile)
    posts_authored = Post.objects.filter(author=request.user.profile)
    posts = []

    # posts commented on by user
    for comment in comments:
        if comment.post in posts:
            continue
        else:
            posts.append(comment.post)

    return render(request, 'profile.html', {
        'posts': posts,
        'posts_authored': posts_authored,
    })