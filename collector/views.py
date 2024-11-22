from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = 'collector/home.html'


