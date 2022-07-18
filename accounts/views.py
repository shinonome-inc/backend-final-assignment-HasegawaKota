from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DetailView,
    ListView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.http import Http404, HttpResponseRedirect

from .models import User, Profile, FriendShip
from tweets.models import Tweet
from .forms import SignupForm, LoginForm, ProfileForm


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "accounts/signup.html"
    # success_url = reverse_lazy("app名:urls.pyで設定したname")
    success_url = reverse_lazy("accounts:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        raw_pass = form.cleaned_data.get("password1")
        user = authenticate(username=username, email=email, password=raw_pass)
        if user is not None:
            login(self.request, user)
            return response


class Login(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class Logout(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"


class UserProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts/profile.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.object.user
        context["tweets_list"] = Tweet.objects.select_related("user").filter(user=user)
        context["following_count"] = (
            FriendShip.objects.select_related("follower", "following")
            .filter(follower=user)
            .count()
        )
        context["follower_count"] = (
            FriendShip.objects.select_related("follower", "following")
            .filter(following=user)
            .count()
        )
        context["flag"] = FriendShip.objects.select_related(
            "follower", "following"
        ).filter(follower=self.request.user, following=user).exists()

        return context


class UserProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile_edit.html"

    def get_success_url(self):
        return reverse("accounts:user_profile", kwargs={"pk": self.object.pk})

    def test_func(self):
        # pkが現在ログイン中ユーザと同じならOK。
        current_user = self.request.user
        return current_user.pk == self.kwargs["pk"]


class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "accounts/home.html"
    context_object_name = "tweets_list"

    def get_queryset(self):
        return Tweet.objects.all().select_related("user")


class WelcomeView(TemplateView):
    template_name = "welcome/index.html"


class FollowView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        follower = self.request.user
        try:
            following = User.objects.get(username=self.kwargs["username"])
            if follower == following:
                messages.warning(request, "自分自身はフォローできない")
                return render(request, "accounts/home.html", status=200)
            elif FriendShip.objects.filter(
                follower=follower, following=following
            ).exists():
                messages.success(request, f"{following.username}は既にフォローしてるだろ！！！！")
                return render(request, "accounts/home.html", status=200)
            else:
                FriendShip.objects.get_or_create(follower=follower, following=following)
                messages.info(request, f"あなたは{following.username}をフォローしました")

        except User.DoesNotExist:
            messages.warning(request, "指定のユーザーは存在しません")
            raise Http404
        return HttpResponseRedirect(reverse("accounts:home"))


class UnFollowView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        follower = self.request.user
        try:
            following = User.objects.get(username=self.kwargs["username"])
            if follower == following:
                messages.warning(request, "自分自身のフォローを外せません")
                return render(request, "accounts/home.html", status=200)
            elif FriendShip.objects.filter(
                follower=follower, following=following
            ).exists():
                FriendShip.objects.filter(
                    follower=follower, following=following
                ).delete()
                messages.success(request, f"あなたは{following.username}のフォローを外しました")
            else:
                messages.warning(
                    request, f"もともと{following.username}をフォローをしてねえから。わかったかクソガキ"
                )
        except User.DoesNotExist:
            messages.warning(request, "指定のユーザーは存在しません")
            raise Http404
        return HttpResponseRedirect(reverse("accounts:home"))


class FollowerListView(LoginRequiredMixin, DetailView):
    template_name = "accounts/follower_list.html"
    model = Profile

    def get_context_data(self, *args, **kwargs):
        user = self.object.user
        context = super().get_context_data(*args, **kwargs)
        context["follower_list"] = FriendShip.objects.select_related("follower").filter(
            following=user
        )
        return context


class FollowingListView(LoginRequiredMixin, DetailView):
    template_name = "accounts/following_list.html"
    model = Profile

    def get_context_data(self, *args, **kwargs):
        user = self.object.user
        context = super().get_context_data(*args, **kwargs)
        context["following_list"] = FriendShip.objects.select_related(
            "following"
        ).filter(follower=user)
        return context
