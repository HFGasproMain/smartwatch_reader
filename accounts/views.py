from django.shortcuts import render, redirect, get_object_or_404
from .forms import HospitalRegistrationForm, AuthenticationForm, ParamedicRegistrationForm, VendorRegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from .utils import is_doctor, is_paramedic, is_vendor, assign_emergency_to_paramedic
from .models import User, Notification, Emergency, Notifications
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
                return redirect('paramedic_dashboard')
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
    notifications_count = Notifications.objects.all().count()
    emergencies = Emergency.objects.all()
    emergencies_count = Emergency.objects.all().count()
    notifications = Notifications.objects.all()

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
        'emergencies':emergencies,
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
    paramedic = request.user
    patients = User.objects.filter(user_type='vendor').count()
    paramedics_count = User.objects.filter(user_type='paramedic').count()
    paramedics = User.objects.filter(user_type='paramedic').all()
    emergencies_count = Emergency.objects.all().count()
    pending_emergencies_count = Emergency.objects.filter(status='pending').count()
    notifications_count = Notifications.objects.all().count()
    emergencies = Emergency.objects.all()
    assigned_emergencies = Emergency.objects.filter(paramedic=paramedic)
    #patient_diagnosis = PatientDiagnosis.objects.all()
    context = {
        'emergencies_count':emergencies_count,
        'notifications_count':notifications_count,
        'patients':patients,
        'paramedics':paramedics,
        'paramedic':paramedic,
        'paramedics_count':paramedics_count,
        'emergencies':emergencies,
        'assigned_emergencies':assigned_emergencies,
        'pending_emergencies_count':pending_emergencies_count
    }

    return render(request, 'paramedic_dashboard.html', context)


@login_required
@user_passes_test(is_paramedic, login_url='login')
def paramedic_details_view(request):
    # Retrieve the emergency instance
    #emergency = get_object_or_404(Emergency, id=emergency_id, paramedic=request.user)
    emergencies = Emergency.objects.filter(paramedic=request.user, status='accepted')

    patients = User.objects.filter(user_type='vendor').count()
    paramedics_count = User.objects.filter(user_type='paramedic').count()
    paramedics = User.objects.filter(user_type='paramedic').all()
    emergencies_count = Emergency.objects.all().count()
    notifications_count = Notifications.objects.all().count()
    pending_emergencies_count = Emergency.objects.filter(status='pending').count()

    
    context = {
        'emergencies': emergencies,
        'emergencies_count':emergencies_count,
        'notifications_count':notifications_count,
        'patients':patients,
        'paramedics':paramedics,
        'pending_emergencies_count':pending_emergencies_count
    }
    return render(request, 'paramedic_details.html', context)



def send_notification(start_time, end_time, max_heart_rate, min_heart_rate, calories, user_identifier):
    # Save the notification data
    notification = Notifications.objects.create(
        start_time=start_time,
        end_time=end_time,
        max_heart_rate=max_heart_rate,
        min_heart_rate=min_heart_rate,
        calories=calories,
        user=user_identifier
    )

    return notification



@login_required
@user_passes_test(is_doctor, login_url='login')
def process_csv_data_view(request):
    # Delete existing data from the Notification model
    Notification.objects.all().delete()
    
    with open('/Users/damilare/Documents/Devs/posi/smarthealth/healthdata.csv', 'r') as csvfile:
    #with open('/Users/damilare/Documents/Devs/posi/Takeout/Fit/Daily activity metrics/2023-07-06.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row

        for index in csvreader:

            #print(f'all rows index ==> {index}')
            start_time = index[0]
            print(f'row start_time => {start_time}')
            end_time = index[1]
            move_minutes = float(index[2]) if index[2] else 0.0
            calories = float(index[3]) if index[3] else 0.0
            distance = float(index[4]) if index[4] else 0.0
            heart_points = float(index[5]) if index[5] else 0.0
            heart_minutes = float(index[6]) if index[6] else 0.0
            avg_heart_rate = float(index[7]) if index[7] else 0.0
            max_heart_rate = float(index[8]) if index[8] else 0.0
            min_heart_rate = float(index[9]) if index[9] else 0.0
            avg_speed = float(index[10]) if index[10] else 0.0
            max_speed = float(index[11]) if index[11] else 0.0
            min_speed = float(index[12]) if index[12] else 0.0
            step_count = int(index[13]) if index[13] else 0.0
            
            #print(f'max_heart_rate for index {index} => {max_heart_rate}')
            #print(f'min_heart_rate for index {index} => {max_heart_rate}')
            #print(f'calories for index {index} => {calories}')
            patient = User.objects.filter(user_type='vendor').first()
            user_identifier = patient
            user_location = patient.location
            #print(f'id and loc => {user_identifier} & {user_location}')

            if max_heart_rate == 95:
                print('Found!!!')
                print(f'{avg_heart_rate}, {min_heart_rate}, {max_heart_rate}')
                #break

            # Set conditions to trigger notifications based on the data
            if max_heart_rate >= 100 or min_heart_rate < 50 or calories < 0.5:
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
	notifications = Notifications.objects.all()
	for notification in notifications:
		if notification.max_heart_rate > 100:
			emergency = Emergency.objects.create(notification=notification, 
                issue=f"Patient's heart rate of {notification.max_heart_rate} is high!!!")
		if notification.min_heart_rate < 40:
			emergency = Emergency.objects.create(notification=notification,
                issue=f"Patient's heart rate of {notification.min_heart_rate} is very low!!!")
		if notification.calories > 0.0 and notification.calories < 0.5:
			emergency = Emergency.objects.create(notification=notification,
                issue=f"Patient's body calories of {notification.calories} is very low!!!")
	return HttpResponseRedirect(reverse('doctor_dashboard')) 
           
   



def assign_notification_view(request, notification_id):
    # Retrieve the notification based on the ID
    emergency = Emergency.objects.get(id=notification_id)

    # Find an available paramedic in the same location
    paramedic = User.objects.filter(user_type='paramedic', location=notification.user.location, availability=True).first()

    if paramedic:
        # Assign the emergency to the paramedic
        emergency.paramedic_assigned = paramedic
        emergency.save()

        # Update the paramedic's availability
        paramedic.availability = False
        paramedic.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
@user_passes_test(is_doctor, login_url='login')
def emergency_message_view(request, emergency_id):
    emergency = get_object_or_404(Emergency, id=emergency_id)

    if request.method == 'POST':
        doc_message = request.POST['doc_message']
        emergency.doc_message = doc_message
        emergency.save()
        return redirect('assign_emergency', emergency_id=emergency_id)
    else:
        pass

    context = {
        'emergency': emergency,
    }
    return render(request, 'emergency_message.html', context)


@login_required
@user_passes_test(is_doctor, login_url='login')
def assign_emergency_to_paramedic_view(request, emergency_id):
    # Retrieve the emergency instance
    emergency = Emergency.objects.get(id=emergency_id)
    # Get all available paramedics
    available_paramedics = User.objects.filter(user_type='paramedic', availability=True)
    print(f'para {available_paramedics}')


    if request.method == 'POST':
        paramedic_id = request.POST['paramedic']
        paramedic = get_object_or_404(User, id=paramedic_id)
        emergency.paramedic = paramedic
        emergency.save()

        # Update the availability of the assigned paramedic
        paramedic.availability = False
        paramedic.save()
        return redirect('doctor_dashboard')

    context = {
        'emergency': emergency,
        'paramedics': available_paramedics,
    }
    return render(request, 'assign_emergency.html', context)
   

@login_required
@user_passes_test(is_doctor, login_url='login')
def paramedics_list_view(request):
    doctor = request.user
    # Get all paramedics
    paramedics = User.objects.filter(user_type='paramedic')
    emergencies_count = Emergency.objects.all().count()
    patients = User.objects.filter(user_type='vendor').count()
    # Filter the emergencies assigned to the paramedic
    pending_emergencies = Emergency.objects.filter(status='pending').count()
    context = {
        'paramedics': paramedics,
        #'emergencies': emergencies,
        'doctor':doctor,
        'patients':patients,
        'emergencies_count':emergencies_count,
        'pending_emergencies':pending_emergencies
    }
    return render(request, 'paramedics_list.html', context)


@login_required
@user_passes_test(is_paramedic, login_url='login')
def patient_list_view(request):
    emergencies_count = Emergency.objects.all().count()
    patients_count = User.objects.filter(user_type='vendor').count()
    patients = User.objects.filter(user_type='vendor')
    pending_emergencies = Emergency.objects.filter(status='pending').count()

    context = {
        'patients': patients,
        'patients_count':patients_count,
        'emergencies_count':emergencies_count,
        'pending_emergencies':pending_emergencies

    }
    return render(request, 'patients_list.html', context)



@login_required
@user_passes_test(is_doctor, login_url='login')
def emergency_list_view(request):
    # Get the current logged-in paramedic
    #paramedic = request.user
    doctor = request.user
    emergencies_count = Emergency.objects.all().count()
    patients = User.objects.filter(user_type='vendor').count()
    # Filter the emergencies assigned to the paramedic
    pending_emergencies = Emergency.objects.filter(status='pending').count()
    emergencies = Emergency.objects.all()
    context = {
        'emergencies': emergencies,
        'doctor':doctor,
        'emergencies_count':emergencies_count,
        'pending_emergencies':pending_emergencies,
        'patients':patients
    }
    return render(request, 'emergency_list.html', context)


@login_required
@user_passes_test(is_paramedic, login_url='login')
def accept_or_reject_emergency_view(request, emergency_id):
    # Retrieve the emergency instance
    emergency = Emergency.objects.get(id=emergency_id)

    if request.method == 'POST':
        status = request.POST.get('status')

        if status == 'accept':
            # Update the emergency status to 'accepted'
            emergency.status = 'accepted'
            emergency.save()
        elif status == 'reject':
            # Update the emergency status to 'rejected'
            emergency.status = 'pending'
            emergency.save()

        # Redirect to the emergency detail view
        return redirect('emergency_detail', emergency_id=emergency_id)

    # Render the accept/reject form template
    return render(request, 'accept_reject_emergency.html', {'emergency': emergency})


@login_required
@user_passes_test(is_paramedic, login_url='login')
def accept_emergency_view(request, emergency_id):
    emergency = get_object_or_404(Emergency, id=emergency_id)
    emergency.status = 'accepted'
    emergency.save()
    # Redirect to the emergency detail view or any other desired page
    return redirect('paramedic_dashboard')


@login_required
@user_passes_test(is_paramedic, login_url='login')
def reject_emergency_view(request, emergency_id):
    emergency = get_object_or_404(Emergency, id=emergency_id)
    emergency.status = 'pending'
    emergency.save()
    # Redirect to the paramedic dashboard or any other desired page
    return redirect('paramedic_dashboard')



def emergency_detail_view(request, emergency_id):
    emergency = get_object_or_404(Emergency, id=emergency_id)
    notifications_count = Notifications.objects.all().count()
    emergencies_count = Emergency.objects.all().count()
    patients = User.objects.filter(user_type='vendor').count()
    context = {
        'emergencies_count':emergencies_count,
        'notifications_count':notifications_count,
        'emergency': emergency,
        'patients':patients
    }
    return render(request, 'emergency_detail.html', context)
