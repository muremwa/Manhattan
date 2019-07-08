from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProfileEditForm
from django.shortcuts import render, redirect, reverse
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
            return redirect(reverse('blog:index'))

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


@login_required
def profile_image(request):
    if request.method == "POST":
        image = request.FILES['profile']
        profile = request.user.profile
        profile.image.delete()
        profile.image = image
        profile.save()

    return redirect(reverse('profile'))


@login_required
def edit_user_details(request):
    user_profile = request.user.profile
    if request.method == "POST":
        form = ProfileEditForm(request.POST)

        if form.is_valid():
            request.username = form.cleaned_data['user_name']
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            user_profile.writer_name = form.cleaned_data['pen_name']
            user_profile.bio = form.cleaned_data['bio']

            request.user.save()
            user_profile.save()
        else:
            return render(request, 'profile_edit.html', {
                'form': form,
            })

        return redirect(reverse('profile'))


    else:
        initial_data = {
            'user_name': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'pen_name': user_profile.writer_name,
            'bio': user_profile.bio,
        }
        return render(request, 'profile_edit.html', {
                'form': ProfileEditForm(initial=initial_data),
            })
