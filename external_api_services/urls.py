from django.urls import path

from . import views

urlpatterns = [
    path('city_autocomplete/', views.city_autocomplete, name='city_autocomplete'),
    path('department_autocomplete/', views.department_autocomplete, name='department_autocomplete'),
]
