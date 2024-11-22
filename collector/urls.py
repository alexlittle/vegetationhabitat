from django.urls import path, include

from collector import views

app_name = 'collector'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path("", views.HomeView.as_view(), name="index"),
    path("observation/create", views.RecordObservationView.as_view(), name="create_observation"),
    path("observation/create/success", views.ObservationSuccessView.as_view(), name="create_observation_success"),
]

