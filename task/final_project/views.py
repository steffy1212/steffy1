import os
from datetime import date, time
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.fields import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from .forms import PrescriptionForm, AppointmentForm, BlogForm
from .models import Patient, MedicalHistory, TreatmentPlan, Doctor, Prescription, CustomUser, Facility, \
    BillingStatement, InsuranceInfo, Blog
from .models import Patient, Appointment
from .models import Patient
import final_project.models
from django.shortcuts import render, redirect
from .forms import PatientRegistrationForm


# PATIENT REGISTRATION

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'register_success.html')
    else:
        form = PatientRegistrationForm()
    return render(request, 'register_patient.html', {'form': form})



# APPOINTMENT BOOKING:

from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment
from .forms import AppointmentForm

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'appointment_success.html')
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})


def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            appointment.status = 'Rescheduled'
            appointment.save()
            return render(request, 'reschedule_success.html')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'reschedule_appointment.html', {'form': form})


def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.status = 'Cancelled'
        appointment.save()
        return render(request, 'cancel_success.html')
    return render(request, 'cancel_appointment.html', {'appointment': appointment})



# MEDICAL HISTORY



def view_medical_history(request, patient_id):
    history = get_object_or_404(MedicalHistory, patient__id=patient_id)
    return render(request, 'medical_history.html', {'history': history})


def history_patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'select_patient.html', {'patients': patients})


# HEALTH EDUCATION
import os
import json
from django.shortcuts import render, redirect

FILE = 'health_resources.json'

def load_resources():
    if os.path.exists(FILE):
        with open(FILE, 'r') as f:
            return json.load(f)
    return []

def save_resources(data):
    with open(FILE, 'w') as f:
        json.dump(data, f, indent=4)

def research_view(request):
    resources = load_resources()
    return render(request, 'research.html', {'resources': resources})

def parts_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')

        resources = load_resources()
        resources.append({
            'title': title,
            'content': content,
            'category': category
        })
        save_resources(resources)

        return redirect('/research/')
    return redirect('/research/')

def search_resources(request):
    query = request.GET.get('q', '').strip().lower()
    resources = load_resources()

    if query:
        filtered = [
            res for res in resources
            if query in res['title'].lower() or query in res['content'].lower()
        ]
    else:
        filtered = []

    return render(request, 'research.html', {'resources': filtered, 'search': True, 'keyword': query})

def value_view(request):
    resources = load_resources()
    return render(request, 'value.html', {'resources': resources})



import json
import os

BILLING_FILE = 'billing_data.json'
def load_data(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)
    with open(file, 'r') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def billing_view(request):
    if request.method == 'POST':
        data = {
            'patient_name': request.POST.get('patient_name'),
            'amount': request.POST.get('amount'),
            'date': request.POST.get('date'),
            'status': request.POST.get('status'),
        }

        billing_data = load_data(BILLING_FILE)

        billing_data.append(data)

        save_data(BILLING_FILE, billing_data)
        return redirect('success_page')

    return render(request, 'billing_form.html')

def success_page(request):
    return render(request, 'success_form.html')




# PATIENT MANAGEMENT

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    history = MedicalHistory.objects.filter(patient=patient)
    treatments = TreatmentPlan.objects.filter(patient=patient)
    return render(request, 'patient_detail.html', {
        'patient': patient,
        'histories': history,
        'treatments': treatments
    })


def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    patient.delete()
    return redirect('patient_list')



# APPOINTMENT SCHEDULE
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Appointment

def doctor_schedule(request):
    appointments = Appointment.objects.filter(
        doctor=request.user
    ).select_related('patient').order_by('appointment_date', 'appointment_time')

    return render(request, 'doctor_schedule.html', {
        'appointments': appointments,
        'user_specialty': request.user.doctor.specialty if hasattr(request.user, 'doctor') else ''
    })


# E-PRESCRIBING:

def create_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save()
            meds = prescription.medications.all()
            interactions = [med.interaction_warning for med in meds if med.interaction_warning]

            # Optionally, send to pharmacy (mocked with email here)
            send_mail(
                subject='New Prescription',
                message=f'Prescription for {prescription.patient.name}:\n' +
                        '\n'.join(m.name for m in meds),
                from_email='clinic@example.com',
                recipient_list=['pharmacy@example.com'],
            )

            return render(request, 'prescription_sent.html', {
                'prescription': prescription,
                'interactions': interactions,
            })
    else:
        form = PrescriptionForm()
    return render(request, 'create_prescription.html', {'form': form})


# ADMIN MODULE
# USER MANAGEMENT

def home(request):
    return render(request, 'home.html')

def user_management(request):
    users = User.objects.all()
    custom_users = CustomUser.objects.all()
    context = {
        'users': users,
        'custom_users': custom_users
    }
    return render(request, 'user_management.html', context)

def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})


# FACILITY MANAGEMENT


def facility_view(request):
    facilities = Facility.objects.prefetch_related('departments__resources')
    return render(request, 'facility.html')


# APPOINTMENT MANAGEMENT

def appointment_list(request):
    appointments = Appointment.objects.all().order_by('-appointment_date')
    return render(request, 'appointment_list.html', {'appointments': appointments})

def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form})

def appointment_delete(request, pk):
    appointment = Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('appointment_list')



