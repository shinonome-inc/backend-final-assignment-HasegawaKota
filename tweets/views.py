from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.core.exceptions import PermissionDenied

from tweets.forms import TweetForm
from tweets.models import Tweet
# Create your views here.

class TweetTopView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = 'tweets/tweets_top.html'
    paginate_by = 20

    def get_queryset(self):
        return Tweet.objects.all().select_related('user')#tweet_setかもしれない


class TweetCreateView(LoginRequiredMixin,CreateView):
    model = Tweet
    form_class = TweetForm
    template_name = 'tweets/tweets_create.html'
    def get_success_url(self):
        return reverse('tweet:detail', kwargs={'pk':self.object.pk})

    def form_valid(self, form): 
        form.instance.user = self.request.user
        return super().form_valid(form)

class TweetDetailView(LoginRequiredMixin,DetailView):
    model = Tweet
    template_name = 'tweets/tweets_detail.html'
    


class TweetDeleteView(LoginRequiredMixin,DeleteView):
    model = Tweet
    template_name = 'tweets/tweets_delete.html'
    success_url = reverse_lazy('tweet:top')
   #ログインしているユーザーしか消去できない機能
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied
        
        return obj
        
