from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages

class HomeView(TemplateView):
    template_name = 'collector/home.html'


class Cam1View(LoginRequiredMixin, TemplateView):
    template_name = 'collector/cam-test1.html'

class Cam2View(LoginRequiredMixin, TemplateView):
    template_name = 'collector/cam-test2.html'


class UserLoginView(LoginView):
    template_name = 'collector/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('collector:index')



