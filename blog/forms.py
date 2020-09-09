from django import forms
from .models import Comment, Profile, Post
from pagedown.widgets import PagedownWidget


# comment form
class CommentForm(forms.Form):
    comment_text = forms.CharField(widget=forms.Textarea)
    comment_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'style': 'display: none;'}),)


# profile form
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio', 'image')


# post form
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)
    lead_text = forms.CharField(widget=PagedownWidget)
    class Meta:
        model = Post
        fields = ('name', 'lead_text', 'image', 'image_caption', 'content', 'tags')
