from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.WelcomeView.as_view(), name="welcome"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    # path('', include('django.contrib.auth.urls')),
    path("profile/<int:pk>/", views.UserProfileView.as_view(), name="user_profile"),
    path(
        "profile/<int:pk>/edit/",
        views.UserProfileEditView.as_view(),
        name="user_profile_edit",
    ),
    path('<int:pk>/following_list/', views.FollowingListView.as_view(), name='following_list'),
    path('<int:pk>/follower_list/', views.FollowerListView.as_view(), name='follower_list'),
    path('<str:username>/follow/', views.FollowView.as_view(), name='follow'),
    path('<str:username>/unfollow/', views.UnFollowView.as_view(), name='unfollow'),
]
