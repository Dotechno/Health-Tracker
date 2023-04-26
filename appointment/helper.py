from datetime import datetime
from datetime import timedelta
import copy

# constants
DAYS_IN_WEEK = 7
WEEKS_IN_MONTH = 4
APPOINTMENT_TIME_INTERVAL = 30
DATETIME_FORMAT = '%m/%d/%y %H:%M:%S'
DATE_OF_WEEK_FORMAT = '%A'
DATE_FORMAT = '%m/%d/%y'
TIME_24_FORMAT = '%H:%M:%S'
TIME_12_FORMAT = '%I:%M %p'

# error constants
WORK_SCHEDULE_ERROR = "schedule error"

class Schedule:
    def __init__(self, date, day, slots = [], is_all_selected = False):
        self.date = date
        self.day = day
        self.slots = slots
        self.is_all_selected = is_all_selected
        
        
    def get_day(self):
        return self.day
    
    def get_slots(self):
        return self.slots
    
    def update_slots_date(self, old_date, new_date):
        for i, slot in enumerate(self.slots):
            current_slot = self.slots[i]
            current_slot.set_id(slot.get_id().replace(old_date, new_date))
            
    def select_all_slots(self, status):
        for slot in self.slots:
            if not slot.get_is_reserved():
                slot.set_is_selected(status)
            
    def is_all_selected(self):
        return self.is_all_selected
    
    def set_all_selected(self, status):
        self.is_all_selected = status
    
    def __repr__ (self):
        return f"\nDay : {self.day}\nAll Selected {self.is_all_selected}\nSlots: {self.slots}"
    
class Slot:
    def __init__(self, id, time, is_reserved=False):
        self.id = id
        self.is_reserved = is_reserved
        self.is_selected = False
        self.time = time
        
    def get_id(self):
        return self.id
    
    def set_id(self, new_id):
        self.id = new_id
    
    def get_time(self):
        return self.time
    
    def set_time(self, new_time):
        self.time = new_time
    
    def get_is_reserved(self):
        return self.is_reserved
    
    def set_is_reserved(self, is_reserved):
        self.is_reserved = is_reserved
        
    def get_is_selected(self):
        return self.is_selected
    
    def set_is_selected(self, is_selected):
        self.is_selected = is_selected
        
    def __repr__(self):
        return f"\nid : {self.id}, time = {self.time}, is_selected = {self.is_selected}"
    
    # def __repr__(self):
    #     return f"id : {self.id}, time = {self.time} , res = {self.is_reserved}, sel = {self.is_selected}"


class helper():
    # gets a subarray of any size of an array
    get_subarray = lambda arr, index, size: arr[index*size:(index+1)*size]
    
    def get_selected_appointments(two_month_appointments):
        selected_appointments = []
        for day in two_month_appointments:
            for slot in day.slots:
                if slot.get_is_selected():
                    selected_appointments.append(slot.get_id())
        return selected_appointments
    
    def select_all_week(week):
        for day in week:
            day.select_all_slots(True)
            day.set_all_selected(True)
    
    def select_all_day(data, date, status):
        for day in data:
            if day.date == date:
                day.select_all_slots(status)
                day.set_all_selected(status)
                return
    
    def update_slot(data, slot_id):
        for day in data:
            for slot in day.get_slots():
                if slot.get_id() == slot_id:
                    new_state = not slot.get_is_selected()
                    slot.set_is_selected(new_state)
                    if new_state == False:
                        day.set_all_selected(False)
                    elif all(slot.get_is_selected() for slot in day.get_slots()):
                        day.set_all_selected(True)
                    return
    
    def get_todays_date():
        return datetime.today().strftime(DATE_FORMAT)
    
    def get_todays_datetime():
        return datetime.today().strftime(DATETIME_FORMAT)
    
    def convert_datetime_to_variables(current_datetime):
        datetime_obj = datetime.strptime(current_datetime, DATETIME_FORMAT)
        return [datetime_obj.year, datetime_obj.month, datetime_obj.day,\
                datetime_obj.hour, datetime_obj.minute, datetime_obj.second]

    def get_current_time():
        return datetime.today().strftime(TIME_24_FORMAT)
    
    def string_date_to_obj(current_datetime):
        return datetime.strptime(current_datetime, DATETIME_FORMAT)
    
    def obj_date_to_string(current_datetime):
        return current_datetime.strftime(DATETIME_FORMAT)
    
    def string_time_to_obj(current_time):
        return datetime.strptime(current_time, TIME_24_FORMAT).time()

    def convert_24_to_12_time(current_time):
        time_obj = datetime.strptime(current_time, TIME_24_FORMAT)
        return time_obj.strftime(TIME_12_FORMAT)
    
    def convert_12_to_object(current_time):
        time_obj = datetime.strptime(current_time, TIME_12_FORMAT)
        return time_obj.strftime(TIME_24_FORMAT)
    
    def get_day_of_week(current_date):
        return current_date.strftime(DATE_OF_WEEK_FORMAT)
        
    def get_appointment_slots(start_hour, end_hour, working_days, physcian_appointments):
        day, daily_slots = helper.get_daily_slots(datetime.today(), start_hour, end_hour)
        if day == WORK_SCHEDULE_ERROR:
            return
        
        already_set_appointment = []
        for current_appointment in physcian_appointments:
            already_set_appointment.append(current_appointment.appointment_date_time)
        
        # get the date range from today to 8 weeks out (2 months of appointments)
        start_date = helper.string_date_to_obj(helper.get_todays_datetime())
        end_date = start_date + timedelta(weeks=8)
        
        two_month_appointments = []
        current_date = start_date
        start_date_str = start_date.strftime(DATE_FORMAT)
        
        # create an array consisting of 8 arrays (aka 2D array representing 8 weeks)
        # and populates each week with 7 days of slots (appointment times)
        current_time = helper.string_time_to_obj(helper.get_current_time())
        while current_date <= end_date:
            copy_daily_slots = copy.deepcopy(daily_slots)
            current_date_str = current_date.strftime(DATE_FORMAT)
            # check if the time for the appointments has passed already and block it out if so
            if start_date_str == current_date_str:
                for slot in copy_daily_slots:
                    if helper.string_time_to_obj(helper.convert_12_to_object(slot.get_time())) < current_time:
                        slot.set_is_reserved(True)
                        
            current_day = helper.get_day_of_week(current_date)
            current_schedule = Schedule(current_date_str, current_day, copy_daily_slots)
            current_schedule.update_slots_date(old_date=start_date_str, new_date=current_date_str)
            two_month_appointments.append(current_schedule)
            current_date += timedelta(days=1)
            
            if working_days.find(current_day) == -1:
                for slot in copy_daily_slots:
                     slot.set_is_reserved(True)
                     
            for slot in copy_daily_slots:
                if slot.get_id() in already_set_appointment:
                    slot.set_is_reserved(True)
        
        return two_month_appointments
        
    def get_daily_slots(day, start_hour, end_hour):
        start_date = datetime.combine(day, helper.string_time_to_obj(start_hour))
        end_date = datetime.combine(day, helper.string_time_to_obj(end_hour))
        
        if(start_date > end_date):
            print("Starting time is greater than ending time")
            return WORK_SCHEDULE_ERROR, None
        elif(start_date == end_date):
            print("Starting time is equal to ending time")
            return WORK_SCHEDULE_ERROR, None

        # create a array with 30 minute slots between starting time and ending time
        daily_slots = []
        step = timedelta(minutes=APPOINTMENT_TIME_INTERVAL)
        next_mark = start_date
        while next_mark < end_date:
            daily_slots.append(next_mark)
            next_mark += step
        daily_slots = [Slot(i.strftime(DATETIME_FORMAT), i.strftime(TIME_12_FORMAT), False) for i in daily_slots]
        
        return [day, daily_slots]