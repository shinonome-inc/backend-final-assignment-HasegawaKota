from typing import Any, Dict
from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import TemplateView,CreateView

from accounts.models import User

from .forms import SignupForm


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('home')

    

class HomeView(TemplateView):
    template_name = 'accounts/home.html'

class WelcomeView(TemplateView):
    template_name = 'welcome/index.html'


