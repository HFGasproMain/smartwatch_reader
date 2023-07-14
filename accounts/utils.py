def is_doctor(user):
    return user.user_type == 'doctor'


def is_paramedic(user):
    return user.user_type == 'paramedic'


def is_vendor(user):
    return user.user_type == 'vendor'


def assign_emergency_to_paramedic(emergency):
    # Get the location of the user from the emergency's notification
    user_location = emergency.notification.user.location

    # Find an available paramedic in the same location as the user
    paramedic = User.objects.filter(user_type='paramedic', location=user_location, availability=True).first()
    
    if paramedic:
        # Assign the emergency to the paramedic
        emergency.paramedic = paramedic
        emergency.save()
        
        # Update the availability of the assigned paramedic
        paramedic.availability = False
        paramedic.save()