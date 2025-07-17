from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.template.response import TemplateResponse

from .models import Doctor, Patient, Appointment, MedicalHistory, TreatmentPlan, CustomUser, Department, Resource, \
    Facility, HealthcareProvider, HealthEducationResource, BillingStatement, InsuranceInfo, Blog

models = [Doctor, Patient, Appointment, MedicalHistory, TreatmentPlan]

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass  # Avoid crash on dev reload

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Access Control', {'fields': ('role',)}),
    )

admin.site.register(CustomUser)




class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1

class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')
    inlines = [DepartmentInline]

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility')
    inlines = [ResourceInline]
    list_filter = ('facility',)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'quantity')
    list_filter = ('department__facility',)




admin.site.register(HealthcareProvider)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'appointment_date', 'department', 'provider')




class HealthEducationResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_on')
    search_fields = ('title', 'category')
    list_filter = ('category',)


# admin.site.register(Patient)
admin.site.register(BillingStatement)
admin.site.register(InsuranceInfo)


admin.site.register(Blog)