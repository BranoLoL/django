from django.contrib.auth import views as auth_views
from . import views
from django.urls import path

app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("register/", views.register, name='register'),
]