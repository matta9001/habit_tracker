import time
from datetime import datetime

def get_current_utc():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

# UTC Format: '2023-09-28 14:17:00'
# Calculates the distance in hours from the input and the current time
def hours_since_time(utc_time_str):
    input_time = datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.utcfromtimestamp(time.time())
    time_difference = current_time - input_time
    hours_difference = time_difference.total_seconds() / 3600

    return round(hours_difference)


# Calculates the distance in hours from the two inputs
def compare_utc(utc_time_str_past, utc_time_str_future):
    past = datetime.strptime(utc_time_str_past, '%Y-%m-%d %H:%M:%S')
    future = datetime.strptime(utc_time_str_future, '%Y-%m-%d %H:%M:%S')
    time_difference = future - past
    hours_difference = time_difference.total_seconds() / 3600

    return round(hours_difference)


# Function that finds the longest contiguous streak from the most recent checkin
# This is defined as a smaller than 48 hour window between each sequential checkin
def calculate_streak(utc_list):
    if len(utc_list) <= 1:
        return 0

    streak_index = 0
    utc_list_reversed = utc_list[::-1]
    for i in range(len(utc_list_reversed) - 1):
        hours_difference = compare_utc(utc_list_reversed[i+1], utc_list_reversed[i])
        if hours_difference > 0 and hours_difference <= 48:
            streak_index = i+1
        else:
            break
    
    return compare_utc(utc_list_reversed[streak_index], utc_list_reversed[0])
