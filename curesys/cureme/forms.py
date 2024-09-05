
from django.forms import ModelForm,formset_factory,inlineformset_factory
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateFormUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']
        

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_fname', 'patient_lname', 'patient_dob', 'patient_gender',
                   'patient_contact_no', 'emer_contact_name',
                  'emer_contact_no', 'address']
        
        
class Patient(forms.ModelForm):

        class Meta:
            model = Patient
            fields = '__all__'
            exclude = ['user']
 
class BloodPressureForm(forms.ModelForm):
       class Meta:
           model= BloodPressure
           exclude = ['patient','blood_press_id']
           widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class InsulinForm(forms.ModelForm):
       class Meta:
           model= Insulin
           exclude = ['patient','insulin_id']
           widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class HeartRateForm(forms.ModelForm):
       class Meta:
           model= HeartRate
           exclude = ['patient','heart_rate_id']
           widgets = {
            'datetaken': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class RespirationRate(forms.ModelForm):
       class Meta:
           model= RespirationRate
           exclude = ['patient','resp_rate_id']
           

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'doctor', 'condition']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['duration', 'dosage', 'medications','instructions']
