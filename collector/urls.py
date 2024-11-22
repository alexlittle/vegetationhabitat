from django.urls import path, include

from collector import views

from .forms import UserLoginForm

app_name = 'collector'
urlpatterns = [
    path('login/', views.LoginView.as_view(
            template_name="collector/login.html",
            authentication_form=UserLoginForm
            ), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path("", views.HomeView.as_view(), name="index"),
    path("observation/create", views.RecordObservationView.as_view(), name="create_observation"),
    path("observation/create/success", views.ObservationSuccessView.as_view(), name="create_observation_success"),
]

