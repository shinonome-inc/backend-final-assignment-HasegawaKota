import os

import openai
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, View
from dotenv import load_dotenv

from .forms import ChatForm, TweetForm
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
        context["is_user_liked_for_tweet"] = self.object.like_set.filter(
            user=user
        ).exists()
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
        return JsonResponse(404, safe=False)


class ChatView(View):
    template_name = "tweets/chat.html"
    load_dotenv()

    def render_template(self, context):
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, self.request))

    def get(self, request):
        form = ChatForm()
        context = {"form": form, "chat_results": ""}
        return self.render_template(context)

    def post(self, request):
        form = ChatForm(request.POST)
        if form.is_valid():
            sentence = form.cleaned_data["sentence"]

            # TODO: API\KEYを直接書きこむ事は絶対に避ける！！
            openai.api_key = os.getenv("API_KEY")

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "日本語で応答してください"},
                    {"role": "user", "content": sentence},
                ],
            )

            chat_results = response["choices"][0]["message"]["content"]
        else:
            chat_results = ""

        context = {"form": form, "chat_results": chat_results}
        return self.render_template(context)
