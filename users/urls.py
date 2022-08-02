from django.urls import path

from users import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name="user register"),
    path('login', views.LoginView.as_view(), name="user register")
]
