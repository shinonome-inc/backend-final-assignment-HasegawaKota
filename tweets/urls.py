from django.urls import path

from . import views

app_name = "tweets"
urlpatterns = [
    path("create/", views.TweetCreateView.as_view(), name="create"),
    path("chat/", views.ChatView.as_view(), name="chat"),
    path("<int:pk>/", views.TweetDetailView.as_view(), name="detail"),
    path("<int:pk>/delete/", views.TweetDeleteView.as_view(), name="delete"),
    path("<int:pk>/like/", views.LikeView, name="like"),
    path("<int:pk>/unlike/", views.UnlikeView, name="unlike"),
]
