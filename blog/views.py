# blog/views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse
import random

# Create your views here.
class ShowAllView(ListView):
    '''Define a view class to show all articles'''

    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

class ArticleView(DetailView):
    '''Display a single article'''

    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

class RandomArticleView(DetailView):
    '''Display a single random article'''

    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self):
        '''Return one instance of the Article object selected at random'''

        allArticles = Article.objects.all()

        return random.choice(allArticles)
    
class CreateArticleView(CreateView):
    '''A view to handle the creation of a new article'''
    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new comment'''
        pk = self.kwargs['pk']
        return reverse('article', kwargs={'pk' : pk})
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template'''
        context = super().get_context_data()
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        context['article'] = article
        return context

    
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database.'''

        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        form.instance.article = article

        return super().form_valid(form)