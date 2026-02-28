#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw iFlow Doctor v1.0.0 - Windows/Linux/macOS Installer
"""
import os
import sys
import shutil
import json
import subprocess
from pathlib import Path
import platform


def detect_python_command():
    """Detect the correct Python command for the system"""
    system = platform.system().lower()
    
    if system == 'windows':
        # Windows: try python, then py, then python3
        for cmd in ['python', 'py', 'python3']:
            try:
                result = subprocess.run(
                    [cmd, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    print(f"  ✓ Found Python: {cmd} ({result.stdout.strip()})")
                    return cmd
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
    else:
        # Linux/macOS: try python3, then python
        for cmd in ['python3', 'python']:
            try:
                result = subprocess.run(
                    [cmd, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    print(f"  ✓ Found Python: {cmd} ({result.stdout.strip()})")
                    return cmd
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
    
    return None


def get_skill_dir():
    """Get the skill installation directory"""
    return Path.home() / ".openclaw" / "skills" / "openclaw-iflow-doctor"


def install_skill():
    """Install the skill to OpenClaw skills directory"""
    
    # Detect system
    system = platform.system().lower()
    is_windows = (system == 'windows')
    
    print("=" * 60)
    print("OpenClaw iFlow Doctor v1.0.0 - Installer")
    print(f"Platform: {platform.system()} {platform.release()}")
    print("=" * 60)
    print()
    
    # Step 1: Detect Python
    print("Step 1: Detecting Python installation...")
    python_cmd = detect_python_command()
    if not python_cmd:
        print("  ✗ Error: Python not found!")
        print("  Please install Python 3.8+ and ensure it's in PATH")
        if is_windows:
            print("  Download: https://python.org/downloads")
        return False
    print()
    
    # Step 2: Check current directory
    print("Step 2: Checking skill files...")
    current_dir = Path(__file__).parent.absolute()
    required_files = ['skill.md', 'openclaw_memory.py', 'cases.json', 'config.json']
    
    for file in required_files:
        file_path = current_dir / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} not found in current directory")
            print(f"  Current directory: {current_dir}")
            return False
    print()
    
    # Step 3: Create skill directory
    print("Step 3: Creating skill directory...")
    skill_dir = get_skill_dir()
    skill_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ {skill_dir}")
    print()
    
    # Step 4: Copy files
    print("Step 4: Copying skill files...")
    files_to_copy = [
        'skill.md',
        'openclaw_memory.py',
        'cases.json',
        'config.json',
        'config_checker.py',
        'watchdog.py',
        'iflow_bridge.py',
        'README.md',
    ]
    
    copied = 0
    for filename in files_to_copy:
        src = current_dir / filename
        dst = skill_dir / filename
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✓ {filename}")
            copied += 1
        else:
            print(f"  ⚠ {filename} (optional, skipped)")
    print(f"  Total: {copied} files copied")
    print()
    
    # Step 5: Create records.json if not exists
    print("Step 5: Initializing records database...")
    records_file = skill_dir / "records.json"
    if not records_file.exists():
        from datetime import datetime
        records_data = {
            "version": "1.0.0",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "records": []
        }
        with open(records_file, 'w', encoding='utf-8') as f:
            json.dump(records_data, f, ensure_ascii=False, indent=2)
        print("  ✓ records.json created")
    else:
        print("  ✓ records.json already exists")
    print()
    
    # Step 6: Create launcher script
    print("Step 6: Creating launcher scripts...")
    
    if is_windows:
        # Windows: Create heal.bat
        launcher = skill_dir / "heal.bat"
        with open(launcher, 'w', encoding='utf-8') as f:
            f.write('@echo off\n')
            f.write(f'cd /d "{skill_dir}"\n')
            f.write(f'{python_cmd} openclaw_memory.py %*\n')
        print(f"  ✓ heal.bat created")
        
        # Windows: Create openclaw-doctor.bat
        doctor_launcher = skill_dir / "openclaw-doctor.bat"
        with open(doctor_launcher, 'w', encoding='utf-8') as f:
            f.write('@echo off\n')
            f.write('chcp 65001 >nul\n')
            f.write(f'cd /d "{skill_dir}"\n')
            f.write(f'{python_cmd} openclaw_memory.py %*\n')
        print(f"  ✓ openclaw-doctor.bat created")
    else:
        # Linux/macOS: Create heal.sh
        launcher = skill_dir / "heal.sh"
        with open(launcher, 'w', encoding='utf-8') as f:
            f.write('#!/bin/bash\n')
            f.write(f'cd "{skill_dir}"\n')
            f.write(f'{python_cmd} openclaw_memory.py "$@"\n')
        # Make executable
        os.chmod(launcher, 0o755)
        print(f"  ✓ heal.sh created")
    print()
    
    # Step 7: Test installation
    print("Step 7: Testing installation...")
    try:
        result = subprocess.run(
            [python_cmd, str(skill_dir / "openclaw_memory.py"), "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("  ✓ Skill test passed")
        else:
            print("  ⚠ Skill test warning (non-critical)")
    except Exception as e:
        print(f"  ⚠ Test skipped: {e}")
    print()
    
    # Step 8: Optional - Add to PATH
    if is_windows:
        print("Step 8: PATH configuration (optional)...")
        print("  To use 'heal' command from anywhere:")
        print(f"  1. Add to PATH: {skill_dir}")
        print("  2. Or use the full path shown below")
        print()
    
    # Print completion message
    print("=" * 60)
    print("Installation completed! ✓")
    print("=" * 60)
    print()
    print(f"Skill location: {skill_dir}")
    print()
    print("Usage:")
    if is_windows:
        print("  PowerShell:")
        print(f'    cd "{skill_dir}"')
        print(f'    {python_cmd} openclaw_memory.py --stats')
        print()
        print("  Or double-click: heal.bat")
        print()
        print("  Quick commands:")
        print('    heal.bat --stats              # Show statistics')
        print('    heal.bat --fix "error msg"    # Diagnose and fix')
        print('    heal.bat --list-cases         # List repair cases')
    else:
        print("  Terminal:")
        print(f'    cd {skill_dir}')
        print(f'    ./{python_cmd} openclaw_memory.py --stats')
        print()
        print('    ./heal.sh --stats')
    print()
    print("Integration:")
    print("  The skill auto-activates when OpenClaw detects errors")
    print("  Or manually trigger via: openclaw skills run openclaw-iflow-doctor")
    print()
    
    return True


def create_powershell_profile_function():
    """Optionally create PowerShell profile function (Windows only)"""
    if platform.system().lower() != 'windows':
        return
    
    print("=" * 60)
    print("Optional: PowerShell Profile Function")
    print("=" * 60)
    print()
    print("To use 'heal' command directly in PowerShell:")
    print()
    print("1. Open your PowerShell profile:")
    print("   notepad $PROFILE")
    print()
    print("2. Add this function:")
    print("   function heal {")
    skill_dir = get_skill_dir()
    print(f'       python "{skill_dir}\\openclaw_memory.py" @args')
    print("   }")
    print()
    print("3. Reload profile:")
    print("   . $PROFILE")
    print()
    print("4. Now you can use:")
    print("   heal --stats")
    print("   heal --fix 'gateway crash'")
    print()


if __name__ == "__main__":
    try:
        if install_skill():
            if platform.system().lower() == 'windows':
                create_powershell_profile_function()
            print("✓ Setup complete!")
            sys.exit(0)
        else:
            print("✗ Setup failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)