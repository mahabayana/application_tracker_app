from django.urls import path
from . import views

urlpatterns = [
    #All the urls to all pages
    path('applications/applications/', views.application_list, name='application_list'),
    path('applications/applications/add/', views.add_application, name='add_application'),
    path('applications/applications/delete/', views.delete_application, name='delete_application'),
    path('applications/edit/<int:app_id>/', views.edit_application, name='edit_application'),
    path('application_analysis/', views.application_analysis, name='application_analysis'),
    path('application_analysis/generate_report/', views.generate_report, name='generate_report'),
    path('application_analysis/count_applications/', views.count_applications, name='count_applications'),
    path('application_analysis/generate_report_two/', views.generate_report_two, name='generate_report_two'),
    
]