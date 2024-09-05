
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from django.db import transaction
from .forms import CreateFormUser
from django.forms import formset_factory
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user , allowed_users, mainsd
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .forms import Patient,PatientRegistrationForm, BloodPressureForm, AppointmentForm, InsulinForm, HeartRateForm, PrescriptionForm
from .models import *
from .symptoms import sympList, predd, rnd_forest
import matplotlib.pyplot as plt


@unauthenticated_user 
def registerPage(request):
    user_form = CreateFormUser()
    patient_form = PatientRegistrationForm()

    if request.method == "POST":
        user_form = CreateFormUser(request.POST)
        patient_form = PatientRegistrationForm(request.POST)

        if user_form.is_valid() and patient_form.is_valid():
            try:
                with transaction.atomic():
                    # Save user and patient details
                    user = user_form.save()

                    patient = patient_form.save(commit=False)
                    patient.user = user  # Link the patient to the user
                    patient.save()

                    # Add user to the 'patient' group
                    patient_group = Group.objects.get(name='patient')
                    patient_group.user_set.add(user)

                    messages.success(request, 'Account created for ' + user.username)
                    return redirect('login')

            except Exception as e:
                messages.error(request, f'Error: {e}')
    print(user_form)
    context = {'user_form': user_form, 'patient_form': patient_form}
    return render(request, 'cureme/register.html', context)


# @csrf_exempt
@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # method login
            return redirect('main1')
        else:
            messages.info(request, 'Username or password is incorrect')
    user_form = CreateFormUser()
    patient_form = PatientRegistrationForm()

    if request.method == "POST":
        user_form = CreateFormUser(request.POST)
        patient_form = PatientRegistrationForm(request.POST)

        if user_form.is_valid() and patient_form.is_valid():
            try:
                with transaction.atomic():
                    # Save user and patient details
                    user = user_form.save()

                    patient = patient_form.save(commit=False)
                    patient.user = user  # Link the patient to the user
                    patient.save()

                    # Add user to the 'patient' group
                    patient_group = Group.objects.get(name='patient')
                    patient_group.user_set.add(user)

                    messages.success(request, 'Account created for ' + user.username)
                    return redirect('login')

            except Exception as e:
                messages.error(request, f'Error: {e}')
    print(user_form)
    context = {'user_form': user_form, 'patient_form': patient_form}
    return render(request, 'cureme/login.html', context)

def logOutUser(request):
    logout(request)
    return redirect('login') 

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
# @mainsd()
def main(request):
    context = {}
    # Use a different variable name for the queryset
    return render(request, 'cureme/main.html',context)



@login_required(login_url='login')
def userPage(request):
    is_doctor = request.user.groups.filter(name='doctor').exists()
    username = request.user.username
    
    user_id = request.user.id
    print(user_id)
    # Retrieve the user object based on the username
    user = get_object_or_404(User, username=username)
    # Get the user's ID
    user = request.user
    if is_doctor:
        # Assuming Doctor model has a ForeignKey to User model
        doctor = get_object_or_404(Doctor, user=user)
        # If the user is a doctor, redirect to doctor_interface
        return redirect('doctor_interface', doctor_id=doctor.doctor_id)
    
    # Assuming Patient model has a ForeignKey to User model
    user_patient = Patient.objects.filter(user=user.id).first()
    
    # Filter prescriptions and appointments related to the user_patient
    prescriptions = Prescription.objects.filter(patient=user_patient)
    user_appointments = Appointment.objects.filter(patient=user_patient)
    
    print(user_appointments)
    context = {'user_patient': user_patient,
               'is_doctor': is_doctor,
               'prescriptions': prescriptions,
               'user_appointments': user_appointments}
    return render(request, 'cureme/user.html', context)


@login_required(login_url='login')
def dash_view(request):
    return render(request, 'cureme/dash.html')



 
def about(response):
    return HttpResponse("aboutpage")











  # Render a page indicating unauthorized access
    
@login_required(login_url='login')
def accounts_view(request):
    username = request.user.username
    
    # Retrieve the user object based on the username
    user = get_object_or_404(User, username=username)
    
    # Get the user's ID
    user = request.user
    user_patient = Patient.objects.filter(user=user).first()
    print(user)
    print(type(user))
    context = {'user': user_patient}
    return render(request, 'cureme/accounts.html',context)





def success_page(request):
    return render(request, 'cureme/waiting/success.html')


@login_required(login_url='login')
def patient_summary(request, user_id):
    username = request.user.username
    # Retrieve the user object based on the username
    user = get_object_or_404(User, username=username)
    # Get the user's ID
    user = request.user
    user_pat = Patient.objects.filter(user=user).first()
    print(user_id)
    print(type(user_id))
    context = {'user_pat': user_pat}
    return render(request, 'cureme/patient/summary.html',context)

def patient_account(request):
    return render(request, 'cureme/patient/account.html')

def home(request):
    return render(request, 'cureme/home.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def patient_vitals(request, user_id):
    # Retrieve the patient associated with the specified user_id
    patient = get_object_or_404(Patient, user__id=user_id)

    # Get existing blood pressure entries for the patient
    blood_pressure_entries = BloodPressure.objects.filter(patient=patient).order_by('-datetime')

    if request.method == 'POST':
        form = BloodPressureForm(request.POST)
        if form.is_valid():
            # Save the blood pressure data to the database
            blood_pressure_instance = form.save(commit=False)
            blood_pressure_instance.patient = patient
            blood_pressure_instance.save()
            messages.success(request, 'Blood Pressure added successfully!')
            return redirect('patient_vitals', user_id=user_id)
    else:
        form = BloodPressureForm()

    # Get existing insulin entries for the patient
    insulin_entries = Insulin.objects.filter(patient=patient).order_by('-datetime')

    if request.method == 'POST':
        insu_form = InsulinForm(request.POST)
        if insu_form.is_valid():
            # Save the blood pressure data to the database
            insulin_instance = insu_form.save(commit=False)
            insulin_instance.patient = patient
            insulin_instance.save()
            messages.success(request, 'Insulin added successfully!')
            return redirect('patient_vitals', user_id=user_id)
    else:
        insu_form = InsulinForm()

    # Get existing heart rate entries for the patient
    heartrate_entries = HeartRate.objects.filter(patient=patient).order_by('-datetaken')

    if request.method == 'POST':
        heart_form = HeartRateForm(request.POST)
        if heart_form.is_valid():
            # Save the blood pressure data to the database
            heartrate_instance = heart_form.save(commit=False)
            heartrate_instance.patient = patient
            heartrate_instance.save()
            messages.success(request, 'Heart Rate added successfully!')
            return redirect('patient_vitals', user_id=user_id)
    else:
        heart_form = HeartRateForm()

    # Get existing insulin entries for the patient
    prescription_entries = Prescription.objects.filter(patient=patient)

    if request.method == 'POST':
        pres_form = PrescriptionForm(request.POST)
        if pres_form.is_valid():
            # Save the blood pressure data to the database
            prescription_instance = pres_form.save(commit=False)
            prescription_instance.patient = patient
            prescription_instance.save()
            messages.success(request, 'Prescription added successfully!')
            return redirect('patient_vitals', user_id=user_id)
    else:
        pres_form = PrescriptionForm()


    context = {'form': form, 'blood_pressure_entries': blood_pressure_entries, 'patient': patient, 'insulin_entries':insulin_entries, 'insu_form':insu_form, 'heartrate_entries':heartrate_entries, 'heart_form':heart_form,'prescription_entries':prescription_entries,'pres_form':pres_form}
    return render(request, 'cureme/patient/vitalss.html', context) 

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def hosp_map(request, user_id):
    # Retrieve the patient associated with the specified user_id
    patient = get_object_or_404(Patient, user__id=user_id)

    # Get existing blood pressure entries for the patient
    test_app_entries = TestAppointment.objects.filter(patient=patient).order_by('-appointment_date')
    context = { 'patient': patient,  'test_app_entries' : test_app_entries }
    return render(request, 'cureme/map.html', context)  

##doctor
@login_required
@allowed_users(allowed_roles=['doctor'])
def doctor_interface(request, doctor_id):
    doctor = Doctor.objects.get(doctor_id=doctor_id)
    doctor_patients_filtered = DoctorPatient.objects.filter(doctor_id=doctor_id)
    patients = [doctor_patient.patient for doctor_patient in doctor_patients_filtered]
    context = {'patients': patients, 'doctor': doctor}
    return render(request, 'cureme/doctor/doctor_interface.html',context)


@login_required
@allowed_users(allowed_roles=['doctor'])
def doctor_patient(request, doctor_id):
    doctor = Doctor.objects.get(doctor_id=doctor_id)
    doctor_patients_filtered = DoctorPatient.objects.filter(doctor_id=doctor_id)
    patients = [doctor_patient.patient for doctor_patient in doctor_patients_filtered]

    blood_pressure_data = []
    for patient in patients:
        latest_bp = BloodPressure.objects.filter(patient=patient).order_by('-datetime').first()
        blood_pressure_data.append({'patient': patient, 'latest_bp': latest_bp})

    context = {'patients': blood_pressure_data, 'doctor': doctor}
    return render(request, 'cureme/doctor/doctor_patient.html', context)

@login_required
@allowed_users(allowed_roles=['patient'])
def book_appointment(request,user_id):
    patient = get_object_or_404(Patient, user__id=user_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment_instance = form.save(commit=False)
            appointment_instance.patient = patient
            appointment_instance.status = 'pending'
            appointment_instance.save()
            messages.success(request, 'Appointment created, please wait for approval.')
            return redirect('Book_Appointment', user_id=user_id)
    else:
        form = AppointmentForm()

    return render(request, 'cureme/patient/bookappt.html', {'form': form})


@login_required
@allowed_users(allowed_roles=['doctor'])
def doctor_action(request, user_id):
    doctor = get_object_or_404(Doctor, user__id=user_id)
    doctor_id = doctor.doctor_id
    doctor_patients_filtered = DoctorPatient.objects.filter(doctor=doctor)
    
    # Extract patient_ids from each patient object
    patient_ids = [doctor_patient.patient.patient_id for doctor_patient in doctor_patients_filtered]
    
    # Retrieve all appointments for the doctor's patients
    appointments = Appointment.objects.filter(patient__patient_id__in=patient_ids)
    
    # Store all appointment values in a list
    appointments1 = []

    for appointment in appointments:
        appointments1.append({
            'patient_fname': appointment.patient.patient_fname,
            'patient_lname': appointment.patient.patient_lname,
            'appointment_date': appointment.appointment_date,
            'condition': appointment.condition,
            'status': appointment.status,
            # Add other appointment details as needed
        })
    
    # print(appointments1)
    # print(type(appointments1))


    return render(request, 'cureme/doctor/appointment_status.html', { 'appointments': appointments1})

@login_required
@allowed_users(allowed_roles=['patient'])
def vital_visualization(request,user_id):
    # Retrieve the patient associated with the specified user_id
    
    return HttpResponse("view using the script")


 


@login_required(login_url='login')
def symp_predict(request):
    
    return render(request, 'cureme/symptom_form.html', {'symptoms2':sympList})

from datetime import date
from django.shortcuts import get_object_or_404

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def pred_value(request):

    if request.method == 'POST':
        # Get the list of selected symptoms from the form
        selected_symptoms = request.POST.getlist('symptoms')
        # Determine the total number of symptoms
        total_symptoms = 17
        
        # Initialize inputsfin as a list of 0s with the same length as the total number of symptoms
        inputsfin = [0] * total_symptoms
        # Fill in the selected symptoms, but only up to the first 17
        for i, symptom in enumerate(selected_symptoms):
            if i >= total_symptoms:
                break
            # Add your logic here to map symptoms to inputsfin indices
            # For example, if symptom is a string, you could do:
            # inputsfin[i] = sympList.index(symptom) if symptom in sympList else 0

        # Convert selected symptoms to a string for display
        selected_symptoms_str = ", ".join(selected_symptoms)
        
        # Get the length of inputsfin
        inputs2 = len(inputsfin)
        
        # Get the number of symptoms in sympList
        num_symptoms = len(sympList)  # Make sure sympList is defined
        
        # Call the predd function with input_args
        prediction = predd(rnd_forest, *inputsfin)  # Make sure rnd_forest is defined
         # Create a new Diagnosis instance and save it
  


        # Render the template with the prediction and other information
        return render(request, 'cureme/prediction_template.html', {
            'selected_symptoms': selected_symptoms_str,
            'inputsfin': inputsfin,
            'inputs2': inputs2,
            'num_symptoms': num_symptoms,
            'prediction': prediction
        })




# # we are doin chartapp from here!!
# def index(request):
#     insulin = Insulin.objects.all()

#     if request.method == 'POST':
#         form = InsulinForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = InsulinForm()

#     context = {
#         "insulin":insulin,
#         "form": form
#     }

#     return render(request, 'cureme/patient/index.html', context)

def index(request):
    # Query the database to retrieve insulin data
    insulin_data = Insulin.objects.all()
    print(insulin_data)
    # Pass the data to the template context
    context = { 
        'insulin_data': insulin_data
    }
    
    # Render the template with the data
    return render(request, 'cureme/patient/index.html', context)