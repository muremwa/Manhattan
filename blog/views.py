from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView, Response
import re
from datetime import datetime

from .forms import CommentForm, PostForm
from .models import Post, Tag, Profile, Comment
from .serializers import PostsSerializer, PostSerializer


# all blog posts
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
def post(request, pk):
    the_post = get_object_or_404(Post, pk=pk)
    tags = the_post.tags.all()

    # get the one with most linked posts
    count = []
    for tag_obj in tags:
        count.append(Post.objects.filter(tags__name__startswith=tag_obj).count())

    the_tag = the_post.tags.all()[count.index(max(count))]
    others = Post.objects.filter(tags__name__startswith=the_tag)
    entries = the_post.entry_set.all()

    # comments
    comments = the_post.comment_set.all()

    comment_form = CommentForm()

    return render(request, 'blog/post.html', {
        'post': the_post,
        'entries': entries,
        'others': others,
        'tags': tags,
        'relation': the_tag,
        'comments': comments,
        'comment_form': comment_form,
    })


# for author
def author(request, pk):
    the_author = get_object_or_404(Profile, pk=pk)
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
    for post_ in posts:
        tags = post_.tags.all()
        # add all rel tags
        for this_tag in tags:
            if this_tag != the_tag:
                if this_tag not in rel_tags:
                    rel_tags.append(this_tag)

    return render(request, 'blog/tag.html', {
        'tag': the_tag,
        'posts': posts,
        'rel_tags': rel_tags,
    })


def search(request):
    query = request.GET.get("q",)

    if query:
        q_set = (
            Q(name__contains=query) |
            Q(author__writer_name__contains=query) |
            Q(tags__name__contains=query)
        )
        results = Post.objects.filter(q_set).distinct()

    else:
        results = []

    return render(request, 'blog/search.html', {
        'query': query,
        'results': results,
    })


# ajax comment
@login_required
def comment(request, post_id):
    the_post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        comment_text = request.POST.get('comment_text')

        new_comment = Comment(
            comment_text=comment_text,
            post=the_post,
            user=request.user.profile
        )
        
        img_present = False
        if 'comment_image' in request.FILES:
            new_comment.comment_image = request.FILES.get('comment_image')
            img_present = True
        
        new_comment.save()

        response = {
            'user': request.user.username,
            'text': new_comment.comment_text,
            'time': new_comment.comment_time,
            'pk': new_comment.pk,
            'img': img_present,
            'del-url': reverse("blog:delete_comment", kwargs={"comment_id": str(new_comment.pk)})
        }
        return JsonResponse(response)


# AJAX delete comment
def delete_comment(request, comment_id):
    comment_ = Comment.objects.get(pk=comment_id)

    if request.user == comment_.user.user or request.user == comment_.post.author.user:
        comment_.delete()

    return JsonResponse({
        'success': True,
    })


# create new posts
class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    permission_required = "blog.add_post"
    template_name = "blog/post_create.html"

    # adding a user
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super(PostCreate, self).form_valid(form)


class PostEdit(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    permission_required = "blog.add_post"
    template_name = "blog/post_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        if context.get('post', None).author.user != self.request.user:
            raise Http404
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = "blog.add_post"
    success_url = reverse_lazy("profile")


# APIs
class PostApiList(ListAPIView):
    # returns all blog posts
    queryset = Post.objects.all()
    serializer_class = PostsSerializer


# returns a specific blog post
class PostApiDetail(APIView):
    @staticmethod
    def clean_date(date):
        match_date = re.findall(r'\d{4}\-\d{2}\-\d{2}', date, re.I | re.M)
        return match_date[0]

    def get(self, request, **kwargs):
        the_post = get_object_or_404(Post, pk=kwargs['pk'])
        data = PostSerializer(the_post).data
        data['date'] = self.clean_date(data['date'])
        return Response(data)
