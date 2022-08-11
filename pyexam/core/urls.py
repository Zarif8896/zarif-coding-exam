from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('all-emp/', views.EmployeeRecords.as_view(), name='all-emp'),
    path('regular-emp/', views.RegularEmployee.as_view(), name='regular-emp'),
    path('country-emp/', views.CountryEmployeeCount.as_view(), name='country-emp'),
    path('dynamic-filter/', views.DynamicEmployeeFilter.as_view(), name='dynamic-filter'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)