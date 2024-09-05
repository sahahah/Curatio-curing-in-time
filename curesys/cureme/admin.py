from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.utils.encoding import smart_bytes

# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'patient_fname', 'patient_lname', 'patient_dob', 'patient_gender', 'patient_contact_no', 'emer_contact_name', 'emer_contact_no', 'address', 'photo', 'patient_email')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='doctor').exists():
            username = request.user.username
            doctor = Doctor.objects.get(user__username=username)
            patient_ids = DoctorPatient.objects.filter(doctor=doctor).values_list('patient_id', flat=True)
            return qs.filter(patient_id__in=patient_ids)
        return qs

admin.site.register(Patient, PatientAdmin)

admin.site.register(Doctor)
admin.site.register(DoctorPatient)
# admin.site.register(Allergy)

def send_email(sender_email, receiver_email, subject, message, app_password):
    # Encode subject and message to ASCII, ignore characters that cannot be encoded
    subject = subject.encode('ascii', 'ignore').decode('ascii')
    message = message.encode('ascii', 'ignore').decode('ascii')

    # Setup the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# Usage example
sender_email = 'kvzui.fx@gmail.com'
# receiver_email = 'sahasrini@gmail.com'
# subject = 'Subject with non-ASCII characters: Café'
# message = 'Message with non-ASCII characters: Café'
app_password = 'fejt grzm lchr iloq'


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'appointment_date', 'patient', 'doctor', 'status')
    list_filter = ('status',)
    actions = ['set_status_approved', 'set_status_declined', 'set_status_pending']
    def save_model(self, request, obj, form, change):
        if change and obj.status == 'APPROVED' and obj.status != form.initial['status']:
            # Send email notification
            sender_email = 'kvzui.fx@gmail.com'
            receiver_email = obj.patient.user.email
            subject = 'Appointment Approved'
            message = 'Your appointment has been approved.'
            subject = subject.encode('ascii', 'ignore').decode('ascii')
            message = message.encode('ascii', 'ignore').decode('ascii')
             # Setup the email
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Attach the message to the email
            msg.attach(MIMEText(message, 'plain'))

            # Send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())


        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='doctor').exists():
            username = request.user.username
            doctor = Doctor.objects.get(user__username=username)
            doctor_patients = DoctorPatient.objects.filter(doctor=doctor).values_list('patient_id', flat=True)
            return qs.filter(patient_id__in=doctor_patients)
        return qs
    
    def set_status_pending(self, request, queryset):
        queryset.update(status='PENDING')
    set_status_pending.short_description = "Set selected appointments to Pending"
    
    def set_status_approved(self, request, queryset):
        queryset.update(status='APPROVED')
        self.message_user(request, f"Updated {queryset.count()} appointments to Approved.")
    set_status_approved.short_description = "Set selected appointments to Approved and send email notifications"

    def set_status_declined(self, request, queryset):
        queryset.update(status='DECLINED')
    set_status_declined.short_description = "Set selected appointments to Declined"

admin.site.register(Appointment, AppointmentAdmin)
##
admin.site.register(BloodPressure)
admin.site.register(Diagnosis)
# admin.site.register(Medication)
# admin.site.register(Immunization)
admin.site.register(Insulin)
admin.site.register(HeartRate)
admin.site.register(Prescription)
admin.site.register(Report)
admin.site.register(RespirationRate)
admin.site.register(Surgery)
# admin.site.register(Oxygen)
admin.site.register(Temperature)

##
admin.site.register(Test)
admin.site.register(TestAppointment)
admin.site.register(Room)
