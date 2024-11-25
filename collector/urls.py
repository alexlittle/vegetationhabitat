from django.urls import path, include
from django.contrib.auth.views import LoginView

from collector import views

from .forms import UserLoginForm

app_name = 'collector'
urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path('login/', LoginView.as_view(
            template_name="collector/login.html",
            authentication_form=UserLoginForm
            ), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),

    path('observation/wizard/', views.ObservationWizard.as_view(), name='observation_wizard'),
    path("observation/wizard/success", views.ObservationSuccessView.as_view(), name="create_observation_success"),
    path("map", views.MapView.as_view(), name="map"),
    path('species-autocomplete/', views.SpeciesAutocompleteView.as_view(), name='species_autocomplete'),
    path('plot-autocomplete/', views.PlotAutocompleteView.as_view(), name='plot_autocomplete'),

    path('profile/observations', views.UserObservationsView.as_view(), name='profile_observations'),
    path('profile/observations/export', views.UserExportObservationsView.as_view(), name='profile_observations_export'),


]

