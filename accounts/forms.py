from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

#CustomUserモデル、DjangoデフォルトのUserモデルを問わず、使用しているUserモデル自体を返してくれる
User=get_user_model

class SignupForm(UserCreationForm):

    class Meta:
       model =User
       
       fields = ('username','password1','password2','email')
      

