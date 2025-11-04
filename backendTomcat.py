import os
import subprocess
import time
import random
import xml.etree.ElementTree as ET


# --- Configuration ---
# Path to your Tomcat installation directory
TOMCAT_HOME = r"C:\apache-tomcat-10.1.30"
SERVER_XML_PATH = os.path.join(TOMCAT_HOME, "conf", "server.xml")
PORT_MIN, PORT_MAX = 8000, 9000


def run_command(command, cwd=None):
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            cwd=cwd
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()


def start_services():
    """Start Tomcat."""
    startup_script = os.path.join(TOMCAT_HOME, "bin", "startup.bat")
    if not os.path.exists(startup_script):
        print("Startup script not found.")
        return
    success, output = run_command(f'cmd /c "{startup_script}"', cwd=TOMCAT_HOME)
    print(output if success else "Failed to start Tomcat.")


def stop_services():
    """Stop Tomcat."""
    shutdown_script = os.path.join(TOMCAT_HOME, "bin", "shutdown.bat")
    if not os.path.exists(shutdown_script):
        print("Shutdown script not found.")
        return
    success, output = run_command(f'cmd /c "{shutdown_script}"', cwd=TOMCAT_HOME)
    print(output if success else "Failed to stop Tomcat.")


def change_port(new_port):
    """Change Tomcat's HTTP connector port in server.xml."""
    if not os.path.exists(SERVER_XML_PATH):
        print("server.xml not found.")
        return False

    tree = ET.parse(SERVER_XML_PATH)
    root = tree.getroot()

    # Find the HTTP connector (protocol="HTTP/1.1")
    for connector in root.iter("Connector"):
        if "protocol" in connector.attrib and "HTTP/1.1" in connector.attrib["protocol"]:
            connector.set("port", str(new_port))
            break

    tree.write(SERVER_XML_PATH)
    print(f"Port updated to {new_port} in server.xml.")
    return True


def change_port_periodically(interval=60):
    """Change Tomcat's HTTP port periodically and restart."""
    while True:
        new_port = random.randint(PORT_MIN, PORT_MAX)
        print(f"Attempting to switch Tomcat port to {new_port}...")
        stop_services()
        time.sleep(3)
        if change_port(new_port):
            start_services()
        time.sleep(interval)
