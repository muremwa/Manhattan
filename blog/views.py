from django.db.transaction import commit
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Post, Tag, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .forms import CommentForm


# all blogs
def index(request):
    posts = Post.objects.all()
    the_query = request.GET.get("query")

    if the_query:
        posts = Post.objects.filter(name__contains=the_query)

    tags = Tag.objects.all()
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
        'the_query':the_query,
    })


# each blog post
# @login_required
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


# for author
def author(request, id):
    the_author = Profile.objects.get(pk=id)
    posts = the_author.post_set.all()

    return render(request, 'blog/author.html', {
        'author':the_author,
        'posts':posts,
    })


# tags
def tags(request):
    the_tags = Tag.objects.all()

    return render(request, 'blog/tags.html', {
        'tags':the_tags,
    })


# each tag
def tag(request, tag_name):
    the_tag = Tag.objects.get(name=tag_name)
    posts = the_tag.post_set.all()

    # related tags
    rel_tags = []
    for post in posts:
        tags = post.tags.all()
        # add all rel tags
        for tag in tags: 
            if tag != the_tag:
                if tag not in rel_tags:
                    rel_tags.append(tag)

    return render(request, 'blog/tag.html', {
        'tag':the_tag,
        'posts':posts,
        'rel_tags':rel_tags,
    })


# comments
def comment(request):
    return render(request, 'blog/comment.html')
