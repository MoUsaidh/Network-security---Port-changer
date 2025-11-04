import subprocess
import time
import os
import random


# --- Configuration ---
# Update this to your Apache config file location
APACHE_CONF_PATH = r"C:\xampp\apache\conf\httpd.conf"
APACHE_SERVICE_NAME = "Apache2.4"  # Or "Apache2.4" / "Apache2" depending on system
PORT_MIN, PORT_MAX = 8000, 9000


def run_command(command):
    """Run system command and return (success, output)."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            check=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()


def start_services():
    """Start Apache service."""
    success, output = run_command(f'net start "{APACHE_SERVICE_NAME}"')
    if success:
        print("Apache started successfully.")
    else:
        print("Failed to start Apache:", output)


def stop_services():
    """Stop Apache service."""
    success, output = run_command(f'net stop "{APACHE_SERVICE_NAME}"')
    if success:
        print("Apache stopped successfully.")
    else:
        print("Failed to stop Apache:", output)


def change_port_periodically(interval=60):
    """
    Change Apache's listening port randomly every `interval` seconds.
    """
    while True:
        new_port = random.randint(PORT_MIN, PORT_MAX)
        if not os.path.exists(APACHE_CONF_PATH):
            print("Apache config file not found.")
            return

        # Read file
        with open(APACHE_CONF_PATH, "r") as f:
            lines = f.readlines()

        # Replace Listen directive
        with open(APACHE_CONF_PATH, "w") as f:
            for line in lines:
                if line.strip().startswith("Listen "):
                    f.write(f"Listen {new_port}\n")
                else:
                    f.write(line)

        print(f"Port changed to {new_port}. Restarting Apache...")
        stop_services()
        time.sleep(3)
        start_services()

        time.sleep(interval)
