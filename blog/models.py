from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    writer_name = models.CharField(max_length=100, default="to be added")
    bio = models.TextField()
    image = models.FileField(null=True, default="default.png")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    # get to individual person
    def get_absolute_url(self):
        return reverse('blog:user', args=[str(self.id)])

    def __str__(self):
        return self.writer_name


# Tags model
class Tag(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    image = models.FileField(null=True)

    # get to individual tag
    def get_absolute_url(self):
        return reverse("blog:tag-detail", args=[str(self.name)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]


# Blog post model
class Post(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True, help_text="Give a name that attracts")
    date = models.DateTimeField(null=False, auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    lead_text = models.TextField(null=True, help_text="Shall appear on index page")
    image = models.FileField(null=True, blank=True)
    image_caption = models.CharField(max_length=100, null=True, blank=True, help_text="Describe the image")
    content = models.TextField(null=True, blank=True, help_text="use MarkDown")
    tags = models.ManyToManyField(Tag, help_text="Select as many as possible")
    likes = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return "{} by {}".format(self.name, self.author)

    # get to individual post
    def get_absolute_url(self):
        return reverse('blog:post', args=[str(self.id)])


    class Meta:
        ordering = ['-date']
        permissions = (('can_create_posts', 'can_manipulate_post'),)


# entry for a post, one post can have many entries
class Entry(models.Model):
    title = models.CharField(max_length=400, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    image = models.FileField(null=True, blank=True)

    def __str__(self):
        return "{} from the post {}".format(self.title, self.post)

    class Meta:
        ordering = ['id']


# comments on post
class Comment(models.Model):
    comment_text = models.CharField(null=False, max_length=140)
    comment_image = models.FileField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    time = models.DateTimeField(null=False, auto_now=True)

    def __str__(self):
        return "Comment by {} on {}".format(self.user, self.post)

    class Meta:
        ordering = ['-time']
