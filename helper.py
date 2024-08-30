import secrets
import os
import requests
from datetime import datetime

def generate_random_state():
    return secrets.token_urlsafe(16)

def get_secret(name, file_extension=".json"):
    filepath = name + file_extension

    if os.path.exists(filepath):
        with open (filepath, "r") as file:
            secret = file.read()
    else:
        secret = os.getenv(name)

    return secret

def get_country(ip_address):
    ip_address = "22.96.191.125"
    URL = f'http://ip-api.com/json/{ip_address}?fields=status,message,country,query'

    response = requests.get(URL)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Access the fields from the JSON response
        status = data.get('status')
        message = data.get('message')
        country = data.get('country')
        query = data.get('query')

        return country
    
    return None

def profile_exists(db, sub):
    collection = db.collection("profiles")

    doc_ref = collection.document(sub)

    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return False

def add_profile_to_db(db, sub, profile_data):
    collection = db.collection("profiles")

    collection.document(sub).set(profile_data)

    return True

def get_current_time():
    return datetime.now()

def get_profile_letter(letter):
    num = 1

    letter = letter.upper()

    if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        letter = "blank"

    path = f'letters/{letter}{num}.png'

    return path