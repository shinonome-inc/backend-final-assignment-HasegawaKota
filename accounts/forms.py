from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Profile

# CustomUserモデル、DjangoデフォルトのUserモデルを問わず、使用しているUserモデル自体を返してくれる
User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label
            # attrsがないとエラーになる


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("introduction", "hobby")
