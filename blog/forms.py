from django import forms
from .models import Comment, Profile, Post
from pagedown.widgets import PagedownWidget


# comment form
class CommentForm(forms.Form):
    comment_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    comment_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'style': 'display: none;'}),)


# post form
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)
    lead_text = forms.CharField(widget=PagedownWidget)
    class Meta:
        model = Post
        fields = ('name', 'lead_text', 'image', 'image_caption', 'content', 'tags')
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'image': forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),
            'image_caption': forms.TextInput(attrs={"class": "form-control"}),
            'tags': forms.SelectMultiple(attrs={"class": "form-control"}),
        }
