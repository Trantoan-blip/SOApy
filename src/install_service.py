"""
Install/Uninstall script for Windows Service
Usage:
  python install_service.py install   - Install the service
  python install_service.py remove    - Remove the service
  python install_service.py start     - Start the service
  python install_service.py stop      - Stop the service
"""

import sys
import os
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    try:
        print(f'Executing: {description}')
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f'✓ {description} successful')
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f'✗ {description} failed')
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f'✗ Error during {description}: {str(e)}')
        return False

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()
    script_dir = Path(__file__).parent
    windows_service_script = script_dir / 'windows_service.py'

    if not windows_service_script.exists():
        print(f'Error: windows_service.py not found in {script_dir}')
        sys.exit(1)

    # Make sure we're running as administrator
    try:
        import ctypes
        is_admin = ctypes.windll.shell.IsUserAnAdmin()
        if not is_admin:
            print('Warning: This script should be run as Administrator')
    except:
        pass

    cmd_map = {
        'install': [sys.executable, str(windows_service_script), 'install'],
        'remove': [sys.executable, str(windows_service_script), 'remove'],
        'start': [sys.executable, str(windows_service_script), 'start'],
        'stop': [sys.executable, str(windows_service_script), 'stop'],
    }

    if command not in cmd_map:
        print(f'Unknown command: {command}')
        print(__doc__)
        sys.exit(1)

    cmd = cmd_map[command]
    desc_map = {
        'install': 'Service installation',
        'remove': 'Service removal',
        'start': 'Service start',
        'stop': 'Service stop',
    }

    if run_command(cmd, desc_map[command]):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
