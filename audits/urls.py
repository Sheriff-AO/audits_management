from django.urls import path
from .views import SiteListView, ClientListView, ChecklistWizardView, VendorCreate, VendorUpdate, ChecklistTwoWizardView, ChecklistThreeWizardView
from .forms import *

from . import views

app_name = 'audits'

urlpatterns = [
    path('', views.index, name='index'),
    path('client/', ClientListView.as_view(), name='client'),
    path('client/<int:pk>/', views.clientDetail, name='client-detail'),
    path('allvendor/', views.AllVendorListView.as_view(), name='all-vendor'),
    path('site/', SiteListView.as_view(), name='site'),
    #path('vendor/', views.vendorList, name='vendor'),
    path('vendor/<int:pk>/', views.vendorDetail, name='vendor-detail'),
    path('create-site', views.createSite, name='create-site'),
    path('create-client/', views.createClient, name='create-client'),
    path('create-vendor/', VendorCreate.as_view(), name='create-vendor'),
    path('update-client/<int:pk>/', views.updateClient, name='update-client'),
    path('delete-client/<int:pk>/', views.deleteClient, name='delete-client'),
    path('update-site/<int:pk>/', views.updateSite, name='update-site'),
    path('delete-site/<int:pk>/', views.deleteSite, name='delete-site'),
    path('update-vendor/<int:pk>/', VendorUpdate.as_view(), name='update-vendor'),
    path('delete-vendor/<int:pk>/', views.deleteVendor, name='delete-vendor'),
    path('site-schedule/', views.createSchedule, name='create-schedule'),
    path('checklist-banks/', ChecklistWizardView.as_view(), name='checklist-banks'),
    path('checklist_fuel&gas-stations/', ChecklistTwoWizardView.as_view(), name='checklist-fuel&gas-stations'),
    path('checklist_c&i/', ChecklistThreeWizardView.as_view(), name='checklist-c&i'),
    path('summary/', views.summary, name='summary'),
  
]
