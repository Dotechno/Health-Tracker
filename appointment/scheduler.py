from .helper import *

def set_up(start_hour, end_hour, working_days, phsycian_appointments):
    today = helper.get_todays_date()
    print(f"Today : {today}")
    
    print(f"Start hour: {start_hour}")
    print(f"End hour: {end_hour}")
    print(f"Working days: {working_days}")
    
    return helper.get_appointment_slots(start_hour, end_hour, working_days, phsycian_appointments)