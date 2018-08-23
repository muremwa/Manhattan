from django import forms
from .models import Comment, Profile


# comment form
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment_text',)


# comments image form
class CommentImageForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment_image',)


# profile form
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio', 'image')
