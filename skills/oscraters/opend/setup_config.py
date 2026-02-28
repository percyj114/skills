#!/usr/bin/env python3
"""
Setup encrypted config file for MooMoo API credentials.
"""
import os
import getpass
from credentials import generate_key, save_encrypted_config

def main():
    password = getpass.getpass("Enter MooMoo API password: ")
    config = {'password': password}
    key = generate_key()
    print("Generated encryption key. Store this securely (e.g., in environment variable MOOMOO_CONFIG_KEY):")
    print(key.decode())
    save_encrypted_config(config, key)
    print("Encrypted config saved to config.enc")

if __name__ == "__main__":
    main()