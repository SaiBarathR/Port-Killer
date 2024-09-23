import os
import psutil
import tkinter as tk
from tkinter import messagebox
import pickle

# Function to kill the port
def kill_port(port, os_type):
    port_found = False
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            for conn in proc.net_connections(kind='inet'):
                if conn.laddr.port == port:
                    port_found = True
                    os.kill(proc.info['pid'], 9)  # Force kill the process
                    return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    return port_found

# Function to handle the kill button click
def on_kill():
    port = int(port_entry.get())
    os_type = os_var.get()
    result = kill_port(port, os_type)
    if result is True:
        messagebox.showinfo("Success", f"Port {port} killed successfully!")
    elif result is False:
        messagebox.showerror("Failure", f"Failed to kill port {port}.")
    else:
        messagebox.showinfo("Info", f"Port {port} is not in use.")

# Function to save preferences
def save_preferences():
    preferences = {
        'port': port_entry.get(),
        'os_type': os_var.get()
    }
    with open('preferences.pkl', 'wb') as f:
        pickle.dump(preferences, f)

# Function to load preferences
def load_preferences():
    if os.path.exists('preferences.pkl'):
        with open('preferences.pkl', 'rb') as f:
            preferences = pickle.load(f)
            port_entry.insert(0, preferences['port'])
            os_var.set(preferences['os_type'])

# Create the main window
root = tk.Tk()
root.title("Port Killer")

# Create and place the widgets
tk.Label(root, text="Port:").grid(row=0, column=0, padx=10, pady=10)
port_entry = tk.Entry(root)
port_entry.grid(row=0, column=1, padx=10, pady=10)

os_var = tk.StringVar(value="Windows")
tk.Label(root, text="OS:").grid(row=1, column=0, padx=10, pady=10)
tk.Radiobutton(root, text="Windows", variable=os_var, value="Windows").grid(row=1, column=1, padx=10, pady=10)
tk.Radiobutton(root, text="Linux", variable=os_var, value="Linux").grid(row=1, column=2, padx=10, pady=10)
tk.Radiobutton(root, text="Mac", variable=os_var, value="Mac").grid(row=1, column=3, padx=10, pady=10)

tk.Button(root, text="Kill Port", command=on_kill).grid(row=2, column=0, columnspan=4, padx=10, pady=10)

# Load preferences on startup
load_preferences()

# Save preferences on close
root.protocol("WM_DELETE_WINDOW", lambda: [save_preferences(), root.destroy()])

# Run the application
root.mainloop()