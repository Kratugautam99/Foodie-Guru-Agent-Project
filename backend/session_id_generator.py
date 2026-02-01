# session id generator module
import random
import string

def generate_random_id(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
session_id = generate_random_id()