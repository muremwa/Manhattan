from django.db.transaction import commit
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Post, Tag, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.views.generic import CreateView
from .forms import CommentForm


# all blogs
def index(request):
    posts = Post.objects.all()
    tags = Tag.objects.all()[:7]
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 4)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', {
        'posts':posts,
        'tags':tags,
    })


# each blog post
def post(request, id):
    post = get_object_or_404(Post, pk=id)
    tags = post.tags.all()

    # get the one with most linked posts
    count = []
    for tag_obj in tags:
        count.append(Post.objects.filter(tags__name__startswith=tag_obj).count())

    tag = post.tags.all()[count.index(max(count))]
    others = Post.objects.filter(tags__name__startswith=tag)
    entries = post.entry_set.all()

    # comments
    comments = post.comment_set.all()

    return render(request, 'blog/post.html', {
        'post':post,
        'entries':entries,
        'others':others,
        'tags':tags,
        'relation':tag,
        'comments':comments,
    })
