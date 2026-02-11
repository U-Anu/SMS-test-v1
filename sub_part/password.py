import random
import string

# def generate_password(length=8):
#     """Generate a random password."""
#     characters = string.ascii_letters + string.digits + string.punctuation
#     return ''.join(random.choice(characters) for _ in range(length))SAFE_SYMBOLS = "!@#$%^&*()_+-=<>?"

SAFE_SYMBOLS = "!@#$%^&*()_+-=<>?"

def generate_password(length=8):
    characters = string.ascii_letters + string.digits + SAFE_SYMBOLS
    return ''.join(random.choice(characters) for _ in range(length))