import random
import string
import requests
import logging

# configure logging (will print to console)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

def generate_random_words(word_count):
    """Generate gibberish random words locally."""
    words = [
        ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        for _ in range(word_count)
    ]
    logging.info(f"Generated {word_count} random words (fallback).")
    return ' '.join(words)


def _fetch_zenquote_text(word_count):
    """Fetch a random quote from ZenQuotes API."""
    url = "https://zenquotes.io/api/random"
    try:
        logging.info(f"Fetching ~{word_count} words from ZenQuotes...")
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        if data and isinstance(data, list) and "q" in data[0]:
            quote = data[0]["q"]
            logging.info(f"Fetched ZenQuote: {quote[:60]}...")
            return " ".join(quote.split()[:word_count])
    except Exception as e:
        logging.error(f"ZenQuotes fetch failed: {e}")
    return None


def _fetch_dummyquote_text(word_count):
    """Fetch a random quote from DummyJSON API."""
    url = "https://dummyjson.com/quotes/random"
    try:
        logging.info(f"Fetching ~{word_count} words from DummyJSON...")
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        quote = data.get("quote", "")
        if quote:
            logging.info(f"Fetched DummyQuote: {quote[:60]}...")
            return " ".join(quote.split()[:word_count])
    except Exception as e:
        logging.error(f"DummyJSON fetch failed: {e}")
    return None


def generate_text(word_count, source='literature'):
    """
    Generate a block of text from APIs or fallback.
    Sources:
      - 'random' : gibberish local random words
      - 'literature' : real quotes (ZenQuotes → DummyJSON → fallback)
    """
    if source == 'literature':
        # Try ZenQuotes first
        api_text = _fetch_zenquote_text(word_count)
        if api_text:
            return api_text

        # Then try DummyJSON
        api_text = _fetch_dummyquote_text(word_count)
        if api_text:
            return api_text

    # fallback
    return generate_random_words(word_count)


# compatibility alias
def generate_random_text(word_count):
    return generate_text(word_count, source='random')


def calculate_accuracy(original_text, user_input):
    original_words = original_text.split()
    user_words = user_input.split()

    correct_words = sum(1 for o, u in zip(original_words, user_words) if o == u)
    accuracy = (correct_words / len(user_words)) * 100 if user_words else 0
    return accuracy


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}:{int(seconds):02d}"
