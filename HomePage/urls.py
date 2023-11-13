from django.urls import path
from . import views


urlpatterns = [
    path('HomePage/',views.Casas_random, name='HomePage'),


]