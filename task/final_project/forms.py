from django import forms
from .models import Prescription, Doctor, Patient, Medication, Appointment, MedicalHistory


class PrescriptionForm(forms.ModelForm):
    medications = forms.ModelMultipleChoiceField(
        queryset=Medication.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Prescription
        fields = ['doctor', 'patient', 'medications', 'notes']

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.all()
        self.fields['patient'].queryset = Patient.objects.all()


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'


class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'contact',]


#
# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['patient_name', 'department', 'provider', 'appointment_date', 'appointment_time']
#
#
# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['patient_name', 'department', 'provider', 'appointment_date', 'appointment_time']
#         widgets = {
#             'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'department': forms.Select(attrs={'class': 'form-select'}),
#             'provider': forms.TextInput(attrs={'class': 'form-control'}),
#             'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#         }



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'department', 'provider', 'appointment_date', 'appointment_time']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }


class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = '__all__'
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'medications': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'allergies': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'treatment_history': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
