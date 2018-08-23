from django.shortcuts import render, get_object_or_404
from .models import Post, Tag, Profile, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, CommentImageForm
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views import generic

# all blogs
def index(request):
    posts = Post.objects.all()
    the_query = request.GET.get("query")
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
        'posts': posts,
        'tags': tags,
        'the_query': the_query,
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

    comment_form = CommentForm()

    return render(request, 'blog/post.html', {
        'post': post,
        'entries': entries,
        'others': others,
        'tags': tags,
        'relation': tag,
        'comments': comments,
        'comment_form': comment_form,
    })


# for author
def author(request, id):
    the_author = get_object_or_404(Profile, pk=id)
    posts = the_author.post_set.all()

    return render(request, 'blog/author.html', {
        'author': the_author,
        'posts': posts,
    })


# tags
class TagsView(generic.ListView):
    template_name = 'blog/tags.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.all()


# each tag
def tag(request, tag_name):
    the_tag = get_object_or_404(Tag, name=tag_name)
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
        'tag': the_tag,
        'posts': posts,
        'rel_tags': rel_tags,
    })


def search(request):
    query = request.GET.get("q",)

    if query:
        qset = (
            Q(name__contains=query) |
            Q(author__writer_name__contains=query) |
            Q(tags__name__contains=query)
        )
        results = Post.objects.filter(qset).distinct()

    else:
        results = []

    return render(request, 'blog/search.html', {
        'query': query,
        'results': results,
    })


# ajax comment
@login_required
def comment(request):
    post = get_object_or_404(Post, pk=request.POST.get('id'))

    if request.method == "POST":
        comment = request.POST['comment']
        user = request.user.profile

        Comment.objects.create(
            comment_text=comment,
            post=post,
            user=user
        )
        return HttpResponse(" ")


# Ajax fetch comments
def all_comments(request):
    the_post = get_object_or_404(Post, pk=request.GET.get('id'))
    comments = the_post.comment_set.filter(user=request.user.profile).values('comment_text', 'post', 'user', 'time')[:1]
    response = {}

    try:
        response['message'] = 'Success from the server!'
        response['results'] = list(comments)
    except:
        response['message'] = 'Failed from the server'
        response['results'] = 'Unexpected error from the server'

    return JsonResponse(response)
