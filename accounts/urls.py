from django.urls import path
from .views import index, hospital_registration_view, paramedic_registration_view, vendor_registration_view, login_view, \
	logout_view, doctor_dashboard_view, process_csv_data_view, vendor_dashboard_view, paramedic_dashboard_view, \
	assign_notification_view, assign_emergency_to_paramedic_view, get_emergency_view, accept_or_reject_emergency_view, \
    emergency_detail_view, accept_emergency_view, reject_emergency_view, emergency_list_view, emergency_message_view, \
    paramedics_list_view, patient_list_view, paramedic_details_view


urlpatterns = [
    # Auth URLs
	path('signup/hospital/', hospital_registration_view, name='hospital_signup'),
	path('signup/paramedic/', paramedic_registration_view, name='paramedic_signup'),
	path('signup/user/', vendor_registration_view, name='vendor_signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Users URLs
    path('hospital/dashboard/', doctor_dashboard_view, name='doctor_dashboard'),
    path('dashboard/', vendor_dashboard_view, name='vendor_dashboard'),
    path('paramedic/dashboard/', paramedic_dashboard_view, name='paramedic_dashboard'),
    path('process-data/', process_csv_data_view, name='process_csv_data'),
    path('assign-paramedic/<int:notification_id>/', assign_notification_view, name='assign-paramedic'),
    path('paramedics/', paramedics_list_view, name='paramedics_list'),
    path('patients/', patient_list_view, name='patient_list'),
    
    # Emergencies URLs
    path('emergencies/<int:emergency_id>/assign/', assign_emergency_to_paramedic_view, name='assign_emergency'),
    path('emergency/<int:emergency_id>/', emergency_message_view, name='emergency_message'),
    path('emergencies/', get_emergency_view, name='get_emergency'),
    path('emergency/list/', emergency_list_view, name='emergency_list'),
    path('emergencies/accept-reject/<int:emergency_id>/', accept_or_reject_emergency_view, name='accept_reject_emergency'),
    path('emergency/<int:emergency_id>/accept/', accept_emergency_view, name='accept_emergency'),
    path('emergency/<int:emergency_id>/reject/', reject_emergency_view, name='reject_emergency'),
    path('emergency/<int:emergency_id>/', emergency_detail_view, name='emergency_detail'),
    path('paramedics/emergencies/', paramedic_details_view, name='paramedic_details'),

]