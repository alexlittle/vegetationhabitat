from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = 'collector/home.html'


class Cam1View(TemplateView):
    template_name = 'collector/cam-test1.html'

class Cam2View(TemplateView):
    template_name = 'collector/cam-test2.html'


