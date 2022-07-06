from django.forms import ModelForm
from django.forms.widgets import Textarea
from .models import Tweet


class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ('contents',)
        # カンマがないとえらーになるのなんで？
        widgets = {'contents': Textarea(attrs={'placeholder': 'ツイート'})}
