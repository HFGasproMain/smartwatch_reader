from django.urls import path
from .views import index, hospital_registration_view, paramedic_registration_view, vendor_registration_view, login_view, \
	logout_view, doctor_dashboard_view, process_csv_data_view, vendor_dashboard_view, paramedic_dashboard_view, \
	assign_notification_view, assign_emergency_to_paramedic_view, get_emergency_view


urlpatterns = [
	path('signup/hospital/', hospital_registration_view, name='hospital_signup'),
	path('signup/paramedic/', paramedic_registration_view, name='paramedic_signup'),
	path('signup/user/', vendor_registration_view, name='vendor_signup'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('hospital/dashboard/', doctor_dashboard_view, name='doctor_dashboard'),
    path('dashboard/', vendor_dashboard_view, name='vendor_dashboard'),
    path('paramedic/dashboard/', paramedic_dashboard_view, name='paramedic_dashboard'),
    path('process-data/', process_csv_data_view, name='process_csv_data'),
    path('assign-paramedic/<int:notification_id>/', assign_notification_view, name='assign-paramedic'),
    path('emergencies/<int:emergency_id>/assign/', assign_emergency_to_paramedic_view, name='assign_emergency'),
    path('emergencies/', get_emergency_view, name='get_emergency'),

]