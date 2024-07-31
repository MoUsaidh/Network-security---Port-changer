import tkinter as tk
from tkinter import ttk
import backendApache  # Import the backend module for Apache service
# Import the backend module for SSH service

apache_var = None
ssh_var = None
output_text = None


def startSelectedServices():
    global apache_var, ssh_var
    if apache_var.get():
        start_apache_service()
    if ssh_var.get():
        start_ssh_service()

def start_apache_service():
    """Start the Apache service."""
    backendApache.start_services()
    updateOutput("Apache service started.")
    backendApache.change_port_periodically()
    

def updateOutput(message):
    """Update the output text with the provided message."""
    global output_text
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, message + "\n")
    output_text.see(tk.END)
    output_text.config(state=tk.DISABLED)








def run_frontend():
    global apache_var, ssh_var, output_text
    root = tk.Tk()
    root.title("Service Manager")

    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=20)

    start_button = ttk.Button(button_frame, text="Start Selected Services", command=startSelectedServices)
    start_button.grid(row=0, column=0, padx=10)

    stop_button = ttk.Button(button_frame, text="Stop Selected Services", command=stopSelectedServices)
    stop_button.grid(row=0, column=1, padx=10)

    service_frame = ttk.Frame(root)
    service_frame.pack(pady=20)

    # Define and grid checkboxes
    apache_var = tk.BooleanVar()
    apache_checkbox = ttk.Checkbutton(service_frame, text="Apache", variable=apache_var)
    apache_checkbox.grid(row=0, column=0, padx=10)

    ssh_var = tk.BooleanVar()
    ssh_checkbox = ttk.Checkbutton(service_frame, text="SSH", variable=ssh_var)
    ssh_checkbox.grid(row=0, column=1, padx=10)

    output_frame = ttk.Frame(root)
    output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    output_text = tk.Text(output_frame, width=50, height=20)
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=output_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text.config(yscrollcommand=scrollbar.set)

    root.mainloop()

if __name__ == "__main__":
    run_frontend()