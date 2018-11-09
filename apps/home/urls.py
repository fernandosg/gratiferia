from django.urls import path
from .views import *
from apps.users.views import ProfileView, ProfileEditView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about", AboutusView.as_view(), name="about_us"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="my_profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="my_profile_edit"),
]
