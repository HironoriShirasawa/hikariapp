from django import forms

from .models import Article, Comment

class ArticleForm(forms.ModelForm):
  class Meta:
    model = Article
    fields = ('title','region','classification','post','article_image')

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('text',)