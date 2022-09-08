from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, DeleteView
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .forms import TweetForm
from .models import Like, Tweet

# Create your views here.


class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    form_class = TweetForm
    template_name = "tweets/tweets_create.html"

    def get_success_url(self):
        return reverse("tweets:detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    template_name = "tweets/tweets_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        like_for_tweet_count = self.object.like_set.count()
        context["like_for_tweet_count"] = like_for_tweet_count
        context["liked_list"] = Like.objects.filter(user=user).values_list(
            "tweet", flat=True
        )
        context["is_user_liked_for_tweet"] = self.object.like_set.filter(user=user).exists()
        return context


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = "tweets/tweets_delete.html"
    success_url = reverse_lazy("accounts:home")

    def test_func(self):
        if Tweet.objects.filter(pk=self.kwargs["pk"]).exists():
            current_user = self.request.user
            tweet_user = Tweet.objects.get(pk=self.kwargs["pk"]).user
            return current_user == tweet_user
        else:
            return Http404


@login_required
def LikeView(request, pk, *args, **kwargs):

    tweet = get_object_or_404(Tweet, pk=pk)
    Like.objects.get_or_create(user=request.user, tweet=tweet)
    context = {
        "like_for_tweet_count": tweet.like_set.count(),
        "tweet_pk": tweet.pk,
    }
    return JsonResponse(context)


@login_required
def UnlikeView(request, pk, *args, **kwargs):

    tweet = get_object_or_404(Tweet, pk=pk)
    like = Like.objects.filter(user=request.user, tweet=tweet)

    if like.exists():
        like.delete()
        context = {
            "like_for_tweet_count": tweet.like_set.count(),
            "tweet_pk": tweet.pk,
        }
        return JsonResponse(context)
    else:
        return JsonResponse(404)
