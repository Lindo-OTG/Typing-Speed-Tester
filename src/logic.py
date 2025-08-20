import time

def calculate_typing_speed(start_time, end_time, text_length):
    time_taken = end_time - start_time  # in seconds
    speed = (text_length / time_taken) * 60  # words per minute
    return speed

def compare_texts(original_text, user_input):
    return original_text == user_input

def track_time(start_time):
    return time.time() - start_time  # returns elapsed time in seconds