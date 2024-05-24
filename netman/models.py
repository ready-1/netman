import os
import yaml
from werkzeug.security import generate_password_hash, check_password_hash

def load_users():
    file_path = os.path.join(os.path.dirname(__file__), 'users.yaml')
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)['users']

users = load_users()

class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get(cls, username):
        user_data = users.get(username)
        if user_data:
            return cls(username, user_data['password'])
        return None