from symtable import Class

from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    title = forms.CharField(help_text='max 200 znaków')

    class Meta:
        model = Post
        fields = [ 'title', 'text', 'image','video']


class CommentForm(forms.ModelForm):


    class Meta:
        model = Comment
        fields = [  'comment']