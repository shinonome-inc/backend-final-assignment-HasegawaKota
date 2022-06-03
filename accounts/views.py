
from email.mime import audio
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,CreateView
from accounts.models import User
from .forms import SignupForm
from django.contrib.auth import authenticate,login


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response=super().form_valid(form)
        
        username=form.cleaned_data.get('username')
        email=form.cleaned_data('email')
        raw_pass=form.cleaned_data.get('password1')
        User=authenticate(username=username,email=email,password=raw_pass)
        login(response,User)
        return response
        

    

class HomeView(TemplateView):
    template_name = 'accounts/home.html'

class WelcomeView(TemplateView):
    template_name = 'welcome/index.html'


