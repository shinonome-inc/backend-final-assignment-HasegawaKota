
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .models import Profile

#CustomUserモデル、DjangoデフォルトのUserモデルを問わず、使用しているUserモデル自体を返してくれる
User = get_user_model()


class SignupForm(UserCreationForm):

    class Meta:
       model = User
       fields = ('username', 'password1', 'password2', 'email')

class LoginForm(AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)#selfあったらエラーになる。
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            #attrsがないとエラーになる

    class Meta:
        fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ('introduction','hobby')
