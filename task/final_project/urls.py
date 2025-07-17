from django.urls import path, include
from . import views

urlpatterns = [
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('doctor/schedule/', views.doctor_schedule, name='doctor_schedule'),
    path('prescription/create/', views.create_prescription, name='create_prescription'),
     path('', views.home, name='home'),
    path('home/', views.home),
    path('user_list/', views.user_list, name='user_list'),
    path('user_management/', views.user_management, name='user_management'),

path('facility/', views.facility_view, name='facility'),


path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/new/', views.appointment_create, name='appointment_create'),
    path('appointments/delete/<int:pk>/', views.appointment_delete, name='appointment_delete'),

    path('patients/register/', views.register_patient, name='register_patient'),


path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/reschedule/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
    path('appointments/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),

path('patients/history/', views.history_patient_list, name='history_patient_list'),
path('patients/history/<int:patient_id>/', views.view_medical_history, name='view_medical_history'),

    path('research/', views.research_view, name='research'),
    path('parts/', views.parts_view, name='parts'),
    path('search/', views.search_resources, name='search_resources'),
    path('value/', views.value_view, name='value'),

    path('billing/', views.billing_view, name='billing_form'),
    path('success/', views.success_page, name='success_page'),





]