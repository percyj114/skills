import os
import sys
import json
import requests
import subprocess
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.absolute()
APP_DIR = BASE_DIR / "app"
BIN_PATH = APP_DIR / "pentaract"
ENV_PATH = APP_DIR / ".env"
TOKEN_PATH = APP_DIR / ".token"
API_URL = "http://localhost:8000/api"

def run_command(cmd, cwd=None):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)

def setup():
    """Install dependencies and build Pentaract."""
    print("Checking dependencies...")
    os.makedirs(APP_DIR, exist_ok=True)
    
    # Check for pre-compiled binary
    PRECOMPILED = BASE_DIR / "assets" / "bin" / "linux-x64" / "pentaract"
    if os.path.exists(PRECOMPILED):
        print("Using pre-compiled binary for Linux x64...")
        run_command(f"cp {PRECOMPILED} {APP_DIR}/")
        run_command(f"chmod +x {APP_DIR}/pentaract")
    else:
        if not os.path.exists(BASE_DIR / "source"):
            print("Cloning Pentaract...")
            run_command(f"git clone https://github.com/Dominux/Pentaract.git {BASE_DIR}/source")
        
        print("Building Backend...")
        run_command("cargo build --release", cwd=BASE_DIR / "source" / "pentaract")
        run_command(f"cp {BASE_DIR}/source/pentaract/target/release/pentaract {APP_DIR}/")

    # UI build still needed or pre-compiled
    if os.path.exists(BASE_DIR / "source" / "ui"):
        print("Building UI...")
        run_command("pnpm install && pnpm run build", cwd=BASE_DIR / "source" / "ui")
        os.makedirs(APP_DIR / "ui", exist_ok=True)
        run_command(f"cp -r {BASE_DIR}/source/ui/dist/* {APP_DIR}/ui/")
    
    print("Setup complete. Use 'init' to configure.")

def init(bot_token, chat_id, email, password):
    """Initialize configuration and database."""
    secret_key = subprocess.check_output("openssl rand -hex 32", shell=True).decode().strip()
    env_content = f"""PORT=8000
WORKERS=4
CHANNEL_CAPACITY=32
SUPERUSER_EMAIL={email}
SUPERUSER_PASS={password}
ACCESS_TOKEN_EXPIRE_IN_SECS=3600
REFRESH_TOKEN_EXPIRE_IN_DAYS=30
SECRET_KEY={secret_key}
TELEGRAM_API_BASE_URL=https://api.telegram.org

DATABASE_USER=pentaract
DATABASE_PASSWORD=pentaract
DATABASE_NAME=pentaract
DATABASE_HOST=localhost
DATABASE_PORT=5432
"""
    with open(ENV_PATH, "w") as f:
        f.write(env_content)
    
    print("Environment configured. Ensure Postgres is running with 'pentaract' user/db.")

def start():
    """Start the Pentaract server."""
    if os.path.exists(APP_DIR / "pid"):
        print("Server might already be running.")
        return
    
    cmd = f"cd {APP_DIR} && set -a && source .env && set +a && ./pentaract > server.log 2>&1 & echo $!"
    pid = subprocess.check_output(cmd, shell=True, executable="/bin/bash").decode().strip()
    with open(APP_DIR / "pid", "w") as f:
        f.write(pid)
    print(f"Server started with PID {pid}")
    time.sleep(2) # Give it a moment to init DB

def stop():
    """Stop the Pentaract server."""
    if os.path.exists(APP_DIR / "pid"):
        with open(APP_DIR / "pid", "r") as f:
            pid = f.read().strip()
        run_command(f"kill {pid}")
        os.remove(APP_DIR / "pid")
        print("Server stopped.")
    else:
        print("No PID file found.")

def login(email, password):
    """Login and save JWT."""
    resp = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
    if resp.status_code == 200:
        token = resp.json().get("access_token")
        with open(TOKEN_PATH, "w") as f:
            f.write(token)
        print("Login successful.")
        return token
    else:
        print(f"Login failed: {resp.text}")
        return None

def get_headers():
    if not os.path.exists(TOKEN_PATH):
        print("Not logged in.")
        sys.exit(1)
    with open(TOKEN_PATH, "r") as f:
        token = f.read().strip()
    return {"Authorization": f"Bearer {token}"}

def list_storages():
    resp = requests.get(f"{API_URL}/storages", headers=get_headers())
    print(json.dumps(resp.json(), indent=2))
    return resp.json()

def upload(storage_id, file_path, remote_path="/"):
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"path": remote_path}
        resp = requests.post(f"{API_URL}/storages/{storage_id}/files/upload", headers=get_headers(), files=files, data=data)
    if resp.status_code in [200, 201]:
        print(f"Uploaded {file_path} to {remote_path}")
    else:
        print(f"Upload failed: {resp.text}")

def download(storage_id, remote_path, local_path):
    resp = requests.get(f"{API_URL}/storages/{storage_id}/files/download/{remote_path}", headers=get_headers())
    if resp.status_code == 200:
        with open(local_path, "wb") as f:
            f.write(resp.content)
        print(f"Downloaded to {local_path}")
    else:
        print(f"Download failed: {resp.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cli.py <command> [args]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "setup":
        setup()
    elif cmd == "init":
        init(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif cmd == "start":
        start()
    elif cmd == "stop":
        stop()
    elif cmd == "login":
        login(sys.argv[2], sys.argv[3])
    elif cmd == "list":
        list_storages()
    elif cmd == "upload":
        upload(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "download":
        download(sys.argv[2], sys.argv[3], sys.argv[4])
