from django.urls import path, include

from collector import views

app_name = 'collector'
urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
]