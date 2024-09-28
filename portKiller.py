import os
import psutil
import tkinter as tk
from tkinter import messagebox, ttk
import pickle

# Function to kill the port
def kill_port(port):
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
    result = kill_port(port)
    if result is True:
        messagebox.showinfo("Success", f"Port {port} killed successfully!")
    elif result is False:
        messagebox.showerror("Failure", f"Failed to kill port {port}.")
    else:
        messagebox.showinfo("Info", f"Port {port} is not in use.")

# Function to show running ports
def show_running_ports():
    for item in ports_tree.get_children():
        ports_tree.delete(item)
    
    for proc in psutil.process_iter(['pid', 'name']):
        for conn in proc.net_connections(kind='inet'):
            ports_tree.insert('', 'end', values=(proc.info['name'], conn.laddr.port))

# Function to kill a specific port
def kill_specific_port(port):
    result = kill_port(port)
    if result is True:
        messagebox.showinfo("Success", f"Port {port} killed successfully!")
    elif result is False:
        messagebox.showerror("Failure", f"Failed to kill port {port}.")
    else:
        messagebox.showinfo("Info", f"Port {port} is not in use.")
    show_running_ports()

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
tk.Button(root, text="Show Running Ports", command=show_running_ports).grid(row=3, column=0, columnspan=4, padx=10, pady=10)

# Frame to display running ports
ports_frame = tk.Frame(root)
ports_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

# Create a Treeview widget
columns = ('name', 'port')
ports_tree = ttk.Treeview(ports_frame, columns=columns, show='headings')
ports_tree.heading('name', text='Name')
ports_tree.heading('port', text='Port')

# Add a vertical scrollbar
scrollbar = ttk.Scrollbar(ports_frame, orient=tk.VERTICAL, command=ports_tree.yview)
ports_tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
ports_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Load preferences on startup
load_preferences()

# Save preferences on close
root.protocol("WM_DELETE_WINDOW", lambda: [save_preferences(), root.destroy()])

# Run the application
root.mainloop()

# import os
# import psutil
# import tkinter as tk
# from tkinter import messagebox, ttk
# import pickle

# # Function to kill the port
# def kill_port(port):
#     port_found = False
#     try:
#         for proc in psutil.process_iter(['pid', 'name']):
#             for conn in proc.net_connections(kind='inet'):
#                 if conn.laddr.port == port:
#                     port_found = True
#                     os.kill(proc.info['pid'], 9)  # Force kill the process
#                     return True
#     except Exception as e:
#         print(f"Error: {e}")
#         return False
#     return port_found

# # Function to handle the kill button click
# def on_kill():
#     port = int(port_entry.get())
#     result = kill_port(port)
#     if result is True:
#         messagebox.showinfo("Success", f"Port {port} killed successfully!")
#     elif result is False:
#         messagebox.showerror("Failure", f"Failed to kill port {port}.")
#     else:
#         messagebox.showinfo("Info", f"Port {port} is not in use.")

# # Function to show running ports
# def show_running_ports():
#     for item in ports_tree.get_children():
#         ports_tree.delete(item)
    
#     for proc in psutil.process_iter(['pid', 'name']):
#         for conn in proc.net_connections(kind='inet'):
#             ports_tree.insert('', 'end', values=(proc.info['name'], conn.laddr.port))

# # Function to kill a specific port
# def kill_specific_port(port):
#     result = kill_port(port)
#     if result is True:
#         messagebox.showinfo("Success", f"Port {port} killed successfully!")
#     elif result is False:
#         messagebox.showerror("Failure", f"Failed to kill port {port}.")
#     else:
#         messagebox.showinfo("Info", f"Port {port} is not in use.")
#     show_running_ports()

# # Function to save preferences
# def save_preferences():
#     preferences = {
#         'port': port_entry.get(),
#         'os_type': os_var.get()
#     }
#     with open('preferences.pkl', 'wb') as f:
#         pickle.dump(preferences, f)

# # Function to load preferences
# def load_preferences():
#     if os.path.exists('preferences.pkl'):
#         with open('preferences.pkl', 'rb') as f:
#             preferences = pickle.load(f)
#             port_entry.insert(0, preferences['port'])
#             os_var.set(preferences['os_type'])

# # Function to filter the treeview
# def filter_treeview():
#     query = search_entry.get().lower()
#     for item in ports_tree.get_children():
#         ports_tree.delete(item)
    
#     for proc in psutil.process_iter(['pid', 'name']):
#         for conn in proc.net_connections(kind='inet'):
#             if query in proc.info['name'].lower() or query in str(conn.laddr.port):
#                 ports_tree.insert('', 'end', values=(proc.info['name'], conn.laddr.port))

# # Function to handle treeview selection
# def on_treeview_select(event):
#     selected_item = ports_tree.selection()[0]
#     selected_port = ports_tree.item(selected_item, 'values')[1]
#     port_entry.delete(0, tk.END)
#     port_entry.insert(0, selected_port)

# # Create the main window
# root = tk.Tk()
# root.title("Port Killer")

# # Create and place the widgets
# tk.Label(root, text="Port:").grid(row=0, column=0, padx=10, pady=10)
# port_entry = tk.Entry(root)
# port_entry.grid(row=0, column=1, padx=10, pady=10)

# os_var = tk.StringVar(value="Windows")
# tk.Label(root, text="OS:").grid(row=1, column=0, padx=10, pady=10)
# tk.Radiobutton(root, text="Windows", variable=os_var, value="Windows").grid(row=1, column=1, padx=10, pady=10)
# tk.Radiobutton(root, text="Linux", variable=os_var, value="Linux").grid(row=1, column=2, padx=10, pady=10)
# tk.Radiobutton(root, text="Mac", variable=os_var, value="Mac").grid(row=1, column=3, padx=10, pady=10)

# tk.Button(root, text="Kill Port", command=on_kill).grid(row=2, column=0, columnspan=4, padx=10, pady=10)
# tk.Button(root, text="Show Running Ports", command=show_running_ports).grid(row=3, column=0, columnspan=4, padx=10, pady=10)

# # Search entry and button
# tk.Label(root, text="Search:").grid(row=4, column=0, padx=10, pady=10)
# search_entry = tk.Entry(root)
# search_entry.grid(row=4, column=1, padx=10, pady=10)
# tk.Button(root, text="Search", command=filter_treeview).grid(row=4, column=2, padx=10, pady=10)

# # Frame to display running ports
# ports_frame = tk.Frame(root)
# ports_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

# # Create a Treeview widget
# columns = ('name', 'port')
# ports_tree = ttk.Treeview(ports_frame, columns=columns, show='headings')
# ports_tree.heading('name', text='Name')
# ports_tree.heading('port', text='Port')

# # Add a vertical scrollbar
# scrollbar = ttk.Scrollbar(ports_frame, orient=tk.VERTICAL, command=ports_tree.yview)
# ports_tree.configure(yscroll=scrollbar.set)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# ports_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# # Bind the treeview selection event
# ports_tree.bind('<<TreeviewSelect>>', on_treeview_select)

# # Load preferences on startup
# load_preferences()

# # Save preferences on close
# root.protocol("WM_DELETE_WINDOW", lambda: [save_preferences(), root.destroy()])

# # Run the application
# root.mainloop()