from django.shortcuts import render, redirect, get_object_or_404
from .forms import HospitalRegistrationForm, AuthenticationForm, ParamedicRegistrationForm, VendorRegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from .utils import is_doctor, is_paramedic, is_vendor, assign_emergency_to_paramedic
from .models import User, Notification, Emergency
import csv

# Create your views here.
def index(request):
    return redirect('login')


def hospital_registration_view(request):
    if request.method == 'POST':
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'doctor'
            user.save()
            
            # Log the user in
            user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('doctor_dashboard')
    else:
        form = HospitalRegistrationForm()
    return render(request, 'doctor_registration.html', {'form': form})


def paramedic_registration_view(request):
    if request.method == 'POST':
        form = ParamedicRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'paramedic'
            user.save()
            
            # Log the user in
            user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('paramedic_dashboard')
    else:
        form = ParamedicRegistrationForm()
    return render(request, 'paramedic_registration.html', {'form': form})


def vendor_registration_view(request):
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'vendor'
            user.save()
            
            # Log the user in
            user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('vendor_dashboard')
    else:
        form = VendorRegistrationForm()
    return render(request, 'vendor_registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'doctor':
                return redirect('doctor_dashboard')
            elif user.user_type == 'paramedic':
                return redirect('patient_dashboard')
            else:
                return redirect('vendor_dashboard')
        else:
            # Handle invalid login
            pass
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@user_passes_test(is_doctor, login_url='login')
def doctor_dashboard_view(request):
    # Retrieve the authenticated doctor user
    doctor = request.user
    patients = User.objects.filter(user_type='vendor').count()
    paramedics = User.objects.filter(user_type='paramedic').count()
    notifications_count = Notification.objects.all().count()
    emergencies = Emergency.objects.all()
    emergencies_count = Emergency.objects.all().count()
    notifications = Notification.objects.all()

    # Configure the number of items per page
    items_per_page = 5
    
    # Create a Paginator object
    paginator = Paginator(emergencies, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page number
    page_obj = paginator.get_page(page_number)
    context = {
        'doctor': doctor,
        'paramedics':paramedics,
        'patients': patients,
        'notifications':notifications,
        'notifications_count':notifications_count,
        'emergencies_count':emergencies_count,
        'page_obj':page_obj
    }

    return render(request, 'doctor_dashboard.html', context)


@login_required
@user_passes_test(is_vendor, login_url='login')
def vendor_dashboard_view(request):
    # Retrieve the authenticated doctor user
    doctor = request.user
    #patient_diagnosis = PatientDiagnosis.objects.all()
    context = {
        'doctor': doctor,
        #,'patient_diagnosis':patient_diagnosis
        #'patients': patients,
    }

    return render(request, 'vendor_dashboard.html', context)


@login_required
@user_passes_test(is_paramedic, login_url='login')
def paramedic_dashboard_view(request):
    # Retrieve the authenticated doctor user
    doctor = request.user
    #patient_diagnosis = PatientDiagnosis.objects.all()
    context = {
        'doctor': doctor,
        #,'patient_diagnosis':patient_diagnosis
        #'patients': patients,
    }

    return render(request, 'paramedic_dashboard.html', context)


@login_required
@user_passes_test(is_doctor, login_url='login')
def process_csv_data_view(request):
    # Delete existing data from the Notification model
    Notification.objects.all().delete()
    with open('/Users/damilare/Documents/Devs/posi/Takeout/Fit/Daily activity metrics/2023-07-06.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row

        for row in csvreader:

            print(f'rows => {row}')
            start_time = row[0]
            print(f'start_time => {start_time}')
            end_time = row[1]
            move_minutes = float(row[2]) if row[2] else 0.0
            calories = float(row[3]) if row[3] else 0.0
            distance = float(row[4]) if row[4] else 0.0
            heart_points = float(row[5]) if row[5] else 0.0
            heart_minutes = float(row[6]) if row[6] else 0.0
            avg_heart_rate = float(row[7]) if row[7] else 0.0
            max_heart_rate = float(row[8]) if row[8] else 0.0
            min_heart_rate = float(row[9]) if row[9] else 0.0
            avg_speed = float(row[10]) if row[10] else 0.0
            max_speed = float(row[11]) if row[11] else 0.0
            min_speed = float(row[12]) if row[12] else 0.0
            step_count = int(row[13]) if row[13] else 0.0
            
            print(f'max_heart_rate => {max_heart_rate}')
            print(f'min_heart_rate => {max_heart_rate}')
            print(f'calories => {calories}')
            patient = User.objects.filter(user_type='vendor').first()
            user_identifier = patient
            user_location = patient.location
            print(f'id and loc => {user_identifier} & {user_location}')

            # Set conditions to trigger notifications based on the data
            if max_heart_rate >= 100 or min_heart_rate < 40 or calories < 0.5:
                # Trigger notification logic here
                send_notification(start_time, end_time, max_heart_rate, min_heart_rate, calories, user_identifier)

    return HttpResponseRedirect(reverse('doctor_dashboard'))
     # Set conditions to trigger notifications based on the data
            # if max_heart_rate >= 100:
            #     # Trigger notification logic here
            #     # You can pass the relevant data to the notification function
            #     send_notification(start_time, end_time, max_heart_rate, min_heart_rate, calories, user_identifier)

            # if min_heart_rate < 40:
            #     send_notification(start_time, end_time, max_heart_rate, calories, min_heart_rate, user_identifier)

            # if calories < 0.5:
            #     send_notification(start_time, end_time, max_heart_rate, min_heart_rate, calories, user_identifier)

            

def get_emergency_view(request):
	notifications = Notification.objects.all()
	for notification in notifications:
		if notification.max_heart_rate > 100:
			emergency = Emergency.objects.create(notification=notification)
		if notification.min_heart_rate < 40:
			emergency = Emergency.objects.create(notification=notification)
		if notification.calories < 0.5:
			emergency = Emergency.objects.create(notification=notification)
	return HttpResponseRedirect(reverse('doctor_dashboard')) 
           
   

def send_notification(start_time, end_time, max_heart_rate, min_heart_rate, calories, user_identifier):
    # Save the notification data
    notification = Notification.objects.create(
        start_time=start_time,
        end_time=end_time,
        max_heart_rate=max_heart_rate,
        min_heart_rate=min_heart_rate,
        calories=calories,
        user=user_identifier
    )

    # Optional: Perform any additional logic or actions related to the notification
    # e.g., notifying the doctor, updating the patient's status, etc.

    # Return the notification object to be used by the doctor for further actions
    return notification


def assign_notification_view(request, notification_id):
    # Retrieve the notification based on the ID
    notification = Notification.objects.get(id=notification_id)

    # Find an available paramedic in the same location
    paramedic = User.objects.filter(user_type='paramedic', location=notification.user.location, availability=True).first()

    if paramedic:
        # Assign the notification to the paramedic
        notification.paramedic_assigned = paramedic
        notification.save()

        # Update the paramedic's availability
        paramedic.availability = False
        paramedic.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def assign_emergency_to_paramedic_view(request, emergency_id):
    # Retrieve the emergency instance
    emergency = Emergency.objects.get(id=emergency_id)

    # Assign the emergency to a paramedic
    assign_emergency_to_paramedic(emergency)

    # Redirect to the desired page (e.g., emergency list or detail view)
    return redirect('emergency_list')