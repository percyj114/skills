#!/usr/bin/env python3
"""Credential helpers for Futu/MooMoo OpenD workflows."""
import getpass
import json
import os

from cryptography.fernet import Fernet

try:
    import keyring
except Exception:  # pragma: no cover - environment dependent
    keyring = None

SERVICE_NAME = 'moomoo_api'
PASSWORD_KEY = 'password'

def get_password_env():
    """Get password from environment variable MOOMOO_PASSWORD."""
    return os.getenv('MOOMOO_PASSWORD')

def get_password_keyring():
    """Get password from Python keyring."""
    if keyring is None:
        raise RuntimeError("python package 'keyring' is not available")

    password = keyring.get_password(SERVICE_NAME, PASSWORD_KEY)
    if not password:
        # Prompt to set it
        password = getpass.getpass("Enter MooMoo API password to store in keyring: ")
        keyring.set_password(SERVICE_NAME, PASSWORD_KEY, password)
    return password

def generate_key():
    """Generate a new encryption key."""
    return Fernet.generate_key()

def encrypt_data(data, key):
    """Encrypt data using the key."""
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data, key):
    """Decrypt data using the key."""
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

def save_encrypted_config(config, key, filepath='config.enc'):
    """Save config to encrypted file."""
    json_data = json.dumps(config)
    encrypted = encrypt_data(json_data, key)
    with open(filepath, 'w') as f:
        f.write(encrypted)

def load_encrypted_config(key, filepath='config.enc'):
    """Load config from encrypted file."""
    with open(filepath, 'r') as f:
        encrypted = f.read()
    json_data = decrypt_data(encrypted, key)
    return json.loads(json_data)

def get_password_config(key, filepath='config.enc'):
    """Get password from encrypted config file."""
    config = load_encrypted_config(key, filepath)
    return config.get('password')

def get_password(method='env'):
    """Get password using specified method."""
    if method == 'env':
        return get_password_env()
    elif method == 'keyring':
        return get_password_keyring()
    elif method == 'config':
        key = os.getenv('MOOMOO_CONFIG_KEY')
        if not key:
            raise ValueError("MOOMOO_CONFIG_KEY not set for config method")
        return get_password_config(key.encode('utf-8'))
    else:
        raise ValueError(f"Unknown method: {method}")

# Example usage:
# password = get_password('env')
# or
# password = get_password('keyring')
# or
# password = get_password('config')
