from django.urls import path

from users import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name="user-register"),
    path('login', views.LoginView.as_view(), name="user-login"),
    path('logout', views.LogoutView.as_view(), name="user-logout"),
    path('change-password', views.PasswordChangeView.as_view(), name="user-change-password"),
    path('user', views.UserView.as_view(), name="user-details"),
]
