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

    path("observation/create/step1", views.ObservationLocationPhotoView.as_view(), name="create_observation"),
    path("observation/create/<int:id>/step2", views.ObservationPlotView.as_view(), name="create_observation_plot"),
    path("observation/create/<int:id>/step3", views.ObservationMeasurementsView.as_view(), name="create_observation_measurements"),
    path("observation/create/<int:id>/step4", views.ObservationSpeciesView.as_view(), name="create_observation_species"),
    path("observation/create/success", views.ObservationSuccessView.as_view(), name="create_observation_success"),
    path("map", views.MapView.as_view(), name="map"),
    path('species-autocomplete/', views.SpeciesAutocompleteView.as_view(), name='species_autocomplete'),
    path('plot-autocomplete/', views.PlotAutocompleteView.as_view(), name='plot_autocomplete'),
]

