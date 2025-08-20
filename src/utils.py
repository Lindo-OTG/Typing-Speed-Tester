import random
import string

def generate_random_text(word_count):
    words = [''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10))) for _ in range(word_count)]
    return ' '.join(words)

def calculate_accuracy(original_text, user_input):
    original_words = original_text.split()
    user_words = user_input.split()
    
    correct_words = sum(1 for o, u in zip(original_words, user_words) if o == u)
    accuracy = (correct_words / len(original_words)) * 100 if original_words else 0
    return accuracy

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}:{int(seconds):02d}"