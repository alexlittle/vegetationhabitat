from django.urls import path, include

from collector import views

app_name = 'collector'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path("", views.HomeView.as_view(), name="index"),
path("cam2", views.Cam2View.as_view(), name="cam2"),
    path("observation/create", views.RecordObservationView.as_view(), name="create_observation"),
]