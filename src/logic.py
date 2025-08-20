import time

def calculate_typing_speed(start_time, end_time, correct_words):
    """
    Calculate words-per-minute (WPM) based on correctly typed words and elapsed time.
    """
    time_taken = end_time - start_time  # seconds
    minutes = time_taken / 60 if time_taken > 0 else 1/60
    speed = correct_words / minutes
    return speed


def compare_texts(original_text, user_input):
    return original_text == user_input


def track_time(start_time):
    return time.time() - start_time  # returns elapsed time in seconds
