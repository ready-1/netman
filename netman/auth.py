import requests
import yaml
from flask import session

# Load configuration
with open('netman/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

BASE_URL = config['api']['base_url']
VERIFY_SSL = config['api']['verify_ssl']

def login_to_api(username, password):
    url = f"{BASE_URL}/login"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload, verify=VERIFY_SSL)
    if response.status_code == 200:
        session['token'] = response.json()['token']
        return True
    return False

def logout_from_api():
    url = f"{BASE_URL}/logout"
    headers = {
        "Authorization": f"Bearer {session.get('token')}"
    }
    response = requests.post(url, headers=headers, verify=VERIFY_SSL)
    if response.status_code == 200:
        session.pop('token', None)
        return True
    return False