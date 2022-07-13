from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
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
from django.http import HttpResponseRedirect

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
        context["tweets_list"] = Tweet.objects.select_related("user").filter(
            user=self.request.user
        )
        context["following_list"] = (
            FriendShip.objects.select_related("follower", "following")
            .filter(follower=self.request.user)
            .count()
        )
        context["follower_list"] = (
            FriendShip.objects.select_related("follower", "following")
            .filter(following=self.request.user)
            .count()
        )

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
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["tweets_list"] = Tweet.objects.select_related("user")
        context["following_list"] = FriendShip.objects.select_related(
            "follower", "following"
        ).filter(follower=self.request.user)
        return context


class WelcomeView(TemplateView):
    template_name = "welcome/index.html"


class FollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follow.html"
    model = FriendShip
    context_object_name = "following_list"

    def post(self, request, *args, **kwargs):
        try:
            follower = get_object_or_404(User, username=self.request.user.username)
            following = get_object_or_404(User, username=self.kwargs["username"])
            if follower == following:
                messages.warning(request, "自分自身はフォローできない")
                follow_flg = (
                    FriendShip.objects.select_related("follower", "following")
                    .filter(follower=self.request.user)
                    .exists()
                )
                context = {"follow_flg": follow_flg}
                return render(request, "accounts/home.html", context, status=200)
            elif FriendShip.objects.filter(
                follower=follower, following=following
            ).exists():
                messages.success(request, f"{following.username}は既にフォローしてるだろ！！！！")
            else:
                FriendShip.objects.get_or_create(follower=follower, following=following)
                messages.warning(request, "あなたは{}をフォローしました".format(following.username))

            return HttpResponseRedirect(reverse_lazy("accounts:home"))
        except User.DoesNotExist:
            messages.warning(request, "{}は存在しません".format(kwargs["username"]))
        return HttpResponseRedirect(reverse_lazy("accounts:home"))


class UnFollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/unfollow.html"
    model = FriendShip

    def post(self, request, *args, **kwargs):
        try:
            follower = get_object_or_404(User, username=self.request.user.username)
            following = get_object_or_404(User, username=self.kwargs["username"])
            if follower == following:
                messages.warning(request, "自分自身のフォローを外せません")
                return render(request, "accounts/home.html", status=200)
            elif FriendShip.objects.filter(
                follower=follower, following=following
            ).exists():
                FriendShip.objects.filter(
                    follower=follower, following=following
                ).delete()
                messages.success(
                    request, "あなたは{}のフォローを外しました".format(following.username)
                )
            else:
                messages.warning(
                    request, "もともと{}をフォローをしてねえから。わかったかクソガキ".format(following.username)
                )

        except User.DoesNotExist:
            messages.warning(request, "{}は存在しません".format(kwargs["username"]))
            return HttpResponseRedirect(reverse_lazy("accounts:home"))

        return HttpResponseRedirect(reverse_lazy("accounts:home"))


class FollowerListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follower_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["follower_list"] = FriendShip.objects.select_related(
            "follower", "following"
        ).filter(following=self.request.user)
        return context


class FollowingListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/following_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["following_list"] = FriendShip.objects.select_related(
            "follower", "following"
        ).filter(follower=self.request.user)
        return context
