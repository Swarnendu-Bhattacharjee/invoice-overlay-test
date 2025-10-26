import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "auth_config.yaml")

def load_auth_config():
    """Load YAML-based authentication config."""
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE) as file:
        return yaml.load(file, Loader=SafeLoader)

def init_auth():
    """Initialize Streamlit Authenticator."""
    config = load_auth_config()
    if not config:
        return None, None, None

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    return authenticator, config

def add_user(username, name, email, password):
    """Add a new user entry to the YAML file (hashed password)."""
    config = load_auth_config() or {
        'credentials': {'usernames': {}},
        'cookie': {'expiry_days': 30, 'key': 'temp_key', 'name': 'pipl_cookie'}
    }

    hashed_pw = stauth.Hasher([password]).generate()[0]
    config['credentials']['usernames'][username] = {
        'name': name,
        'email': email,
        'password': hashed_pw
    }

    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as file:
        yaml.dump(config, file, default_flow_style=False)
    return True
