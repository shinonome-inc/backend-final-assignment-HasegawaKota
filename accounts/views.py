
from django.urls import reverse_lazy
from django.views.generic import TemplateView,CreateView
from django.contrib.auth import authenticate,login

from accounts.models import User
from .forms import SignupForm



class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        raw_pass = form.cleaned_data.get('password1')
        user = authenticate(username=username,email=email,password=raw_pass)
        if user is not None:
            login(self.request,user)
            return response
        

    

class HomeView(TemplateView):
    template_name = 'accounts/home.html'

class WelcomeView(TemplateView):
    template_name = 'welcome/index.html'


