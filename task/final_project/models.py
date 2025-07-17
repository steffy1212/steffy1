from django.contrib.auth.models import AbstractUser, Permission, Group, User
from django.db import models
from pip._internal.utils._jaraco_text import _


# PATIENT MANAGEMENT
class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name
class MedicalHistory(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    allergies = models.TextField()
    surgeries = models.TextField()


class TreatmentPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()


# APPOINTMENT SCHEDULE

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)





class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    provider = models.ForeignKey(User, on_delete=models.CASCADE)  # this is your doctor
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.patient_name} with Dr. {self.provider.get_full_name()} on {self.appointment_date}"

# E-PRESCRIBING:

class Medication(models.Model):
    name = models.CharField(max_length=100)
    interaction_warning = models.TextField(blank=True)  # Optional: warnings

class Prescription(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    medications = models.ManyToManyField(Medication)
    notes = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.name} by {self.doctor.name} on {self.date}"




# USER MANAGEMENT

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        verbose_name=_('groups'),
        help_text=_('The groups this user belongs to.'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        verbose_name=_('user permissions'),
        help_text=_('Specific permissions for this user.'),
    )



class Facility(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.facility.name})"

class Resource(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='resources')
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.department.name}"






class HealthcareProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.get_full_name()

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()

    def __str__(self):
        return f"Appointment with {self.patient_name} on {self.appointment_date}"


appointment_date = models.DateField()
appointment_time = models.TimeField()







class AppointmentForm(models.Model):
    DEPARTMENT_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Neurology', 'Neurology'),
        ('Pediatrics', 'Pediatrics'),
        ('General', 'General Medicine'),
    ]

    patient_name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    provider = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, default='Scheduled')

    def __str__(self):
        return f"{self.patient_name} - {self.appointment_date} at {self.appointment_time}"


class MedicalHistoryForm(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    medications = models.TextField()
    allergies = models.TextField()
    treatment_history = models.TextField()

    def __str__(self):
        return f"Medical History for {self.patient.name}"




class HealthEducationResource(models.Model):
    CATEGORY_CHOICES = [
        ('Nutrition', 'Nutrition'),
        ('Mental Health', 'Mental Health'),
        ('Disease Prevention', 'Disease Prevention'),
        ('Heart Health', 'Heart Health'),
        ('Child Care', 'Child Care'),
        ('Women Health', 'Women Health'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    content = models.TextField()
    published_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class BillingStatement(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    lab_tests = models.DecimalField(max_digits=10, decimal_places=2)
    medications = models.DecimalField(max_digits=10, decimal_places=2)
    room_charges = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    last_payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=100)

    def __str__(self):
        return f"Billing for {self.patient.name}"

class InsuranceInfo(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    provider = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)
    valid_till = models.DateField()
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Insurance of {self.patient.name}"


from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
