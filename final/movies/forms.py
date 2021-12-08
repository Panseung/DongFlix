from django import forms
from django.forms import widgets
from .models import Article, Comment


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        # fields = '__all__'
        fields = ('title', 'content',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ('movie', 'user')
        
        

class SearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')