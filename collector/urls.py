from django.urls import path, include

from collector import views

app_name = 'collector'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path("", views.HomeView.as_view(), name="index"),
    path("cam1test", views.Cam1View.as_view(), name="cam1"),
    path("cam2test", views.Cam2View.as_view(), name="cam2"),
]