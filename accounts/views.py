
from django.urls import reverse_lazy ,reverse

from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login

from accounts.models import User, Profile
from .forms import SignupForm, LoginForm, ProfileForm



class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    #success_url = reverse_lazy("app名:urls.pyで設定したname")
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        raw_pass = form.cleaned_data.get('password1')
        user = authenticate(username=username, email=email, password=raw_pass)
        if user is not None:
            login(self.request, user)
            return response
        
class Login(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/logout.html'

class UserProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

class UserProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'

    def get_success_url(self):
        return reverse('accounts:user_profile', kwargs={'pk':self.object.pk})
        
    def test_func(self):
        # pkが現在ログイン中ユーザと同じならOK。
        current_user = self.request.user
        return current_user.pk == self.kwargs['pk']

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/home.html'
  

class WelcomeView(TemplateView):
    template_name = 'welcome/index.html'
