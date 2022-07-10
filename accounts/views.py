from django.contrib import messages
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
    # context_object_name = 'profile_list'
    template_name = "accounts/profile.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["tweet_list"] = Tweet.objects.select_related("user").filter(
            user=self.request.user
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
    context_object_name = 'tweets_list'

    def get_queryset(self):
        return Tweet.objects.all().select_related("user")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["following_list"] = FriendShip.objects.select_related(
            "follower", "following"
        ).filter(following=self.request.user)
        return context


class WelcomeView(TemplateView):
    template_name = "welcome/index.html"


# follower=俺をフォローしている人
# following=俺がフォローしている人


class FollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follow.html"
    model = FriendShip
    context_object_name = "following_list"

    def post(self, request, *args, **kwargs):
        try:
            follower = User.objects.get(username=self.request.user.username)
            following = User.objects.get(username=self.kwargs["username"])
            if follower == following:
                messages.warning(request, "自分自身はフォローできない")
            else:
                FriendShip.objects.get_or_create(follower=follower, following=following)

                if FriendShip.objects.get_or_create(
                    follower=follower, following=following
                ):
                    messages.success(request, f"{following.username}をフォローしました")
                else:
                    messages.warning(
                        request, "あなたはすでに{}をフォローしています".format(following.username)
                    )

                return HttpResponseRedirect(reverse_lazy("accounts:home"))
        except User.DoesNotExist:
            messages.warning(request, "{}は存在しません".format(kwargs["username"]))
        return HttpResponseRedirect(reverse_lazy("accounts:home"))


# follower=俺をフォローしている人
# following=俺がフォローしている人


class UnFollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/unfollow.html"
    model = FriendShip

    def post(self, request, *args, **kwargs):
        try:
            follower = User.objects.get(username=self.request.user.username)
            following = User.objects.get(username=self.kwargs["username"])
            if follower == following:
                messages.warning(request, "自分自身のフォローを外せません")
            else:
                FriendShip.objects.filter(
                    follower=follower, following=following
                ).delete()
                messages.success(
                    request, "あなたは{}のフォローを外しました".format(following.username)
                )
        except User.DoesNotExist:
            messages.warning(request, "{}は存在しません".format(kwargs["username"]))
            return HttpResponseRedirect(reverse_lazy("accounts:home"))

        # return HttpResponseRedirect(reverse_lazy('accounts:home', kwargs={'username': following.username}))
        return HttpResponseRedirect(reverse_lazy("accounts:home"))


class FollowingListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/following_list.html"
    context_object_name = "following_list"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["following"] = FriendShip.objects.select_related(
            "follower", "following"
        ).filter(following=self.request.user)
        return context


class FollowerListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follower_list.html"
    context_object_name = "follower_list"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["follower"] = Tweet.objects.select_related(
            "follower", "following"
        ).filter(follower=self.request.user)
        return context
