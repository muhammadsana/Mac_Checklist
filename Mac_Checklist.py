#!/usr/local/bin/python3
import tkinter as tk
import re
import subprocess
import time
from tkinter import scrolledtext
from tkinter import messagebox
# Create GUI
root = tk.Tk()
root.title("Mac Computer Information and Status")
# Increase width of the window
root.geometry("750x590")  # Set width to 800 pixels and height to 620 pixels
 
# Function to update components
def update_components():
    # Fetch macOS system sharing name
    system_sharing_name = get_system_sharing_name()
    system_sharing_name_text.set(system_sharing_name)
    # Check if the host is in Active Directory in macOS
    in_ad = is_bound_to_active_directory()
    in_ad_text.set(in_ad)
    # Fetch macOS host name
    host_name = get_host_name()
    host_name_text.set(host_name)
    # Check LAPS status
    laps_status = check_laps_status()
    laps_status_text.set(laps_status)
    # Get admin users
    admin_users_output = get_admin_users()
    # Insert admin users' output into the ScrolledText widget
    admin_users_text.configure(state="normal")
    admin_users_text.delete(1.0, tk.END)
    admin_users_text.insert(tk.END, admin_users_output)
    admin_users_text.configure(state="disabled")
    # Check ATP status
    atp_status = check_atp()
    atp_status_text.set(atp_status)
    # Fetch and display system updates
    updates_display = display_system_updates()
    updates_textbox.configure(state="normal")
    updates_textbox.delete(1.0, tk.END)
    updates_textbox.insert(tk.END, updates_display)
    updates_textbox.configure(state="disabled")
# Function to fetch macOS system sharing name
def get_system_sharing_name():
    try:
        result = subprocess.run(['scutil', '--get', 'ComputerName'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "Error: Unable to retrieve system sharing name"
    except Exception as e:
        return f"Error: {e}"
# Function to fetch macOS host name
def get_host_name():
    try:
        result = subprocess.run(['hostname'], capture_output=True, text=True)
        if result.returncode == 0:
            hostname = result.stdout.strip()
            hostname_without_local = re.sub(r'\.local$', '', hostname)
            return hostname_without_local
        else:
            return "Error: Unable to retrieve hostname"
    except Exception as e:
        return f"Error: {e}"
# Function to check LAPS status
def check_laps_status():
    try:
        lapslog_output = subprocess.check_output("awk 'BEGIN { FS = \"|\" };{if($4 ~ /Password/)print $4}' /Library/Logs/macOSLAPS.log | sort -u", shell=True)
        lapslog_lines = lapslog_output.decode().split('\n')
        LAPSFLAG = 0
        if lapslog_lines[0] == "Password Change is required as the LAPS password for admin, has expired":
            LAPSFLAG = 1
            if lapslog_lines[1] == "Password change has been completed locally. Performing changes to Active Directory":
                LAPSFLAG = 2
                if lapslog_lines[2][:80] == "Password change has been written to Active Directory for the local administrator":
                    LAPSFLAG = 3
        if LAPSFLAG == 0:
            return "FAILURE"
        elif LAPSFLAG == 1:
            return "Detected password change, but didn't change locally."
        elif LAPSFLAG == 2:
            return "Changed password locally, but didn't change on Active Directory."
        elif LAPSFLAG == 3:
            return "Successfully executed changes."
    except Exception as e:
        return f"Error: {e}"
# Function to check if the macOS host is bound to an Active Directory domain
def is_bound_to_active_directory():
    try:
        output = subprocess.check_output(["dsconfigad", "-show"]).decode().strip()
        if "Active Directory Domain" in output:
            return "Bound"
        else:
            return "Not Bound"
    except subprocess.CalledProcessError as e:
        return "Error: Unable to determine Active Directory binding."
    except Exception as e:
        return f"Unexpected error: {e}"
# Function to get all admin users on the system
def get_admin_users():
    try:
        admin_output = subprocess.check_output(["dscl", ".", "-read", "/Groups/admin", "GroupMembership"]).decode()
        admin_users = admin_output.split("GroupMembership: ")[1].strip().split()
        admin_users_string = "\n".join(admin_users)
        return admin_users_string
    except subprocess.CalledProcessError as e:
        return "Error: Unable to retrieve admin users."
    except Exception as e:
        return f"Unexpected error: {e}"
# Function to check ATP status
def check_atp():
    try:
        atp_output = subprocess.check_output(["/usr/local/bin/mdatp", "version"]).decode().strip()
        return f"{atp_output}"
    except subprocess.CalledProcessError as e:
        return f"ATP Check: Failed with error code {e.returncode}"
    except Exception as e:
        return f"Error: {e}"
# Function to retrieve system updates and display them without colorization
def display_system_updates():
    updates_command = "softwareupdate -l | awk '/Label: /{print $3}'"
    updates_output = subprocess.run(updates_command, shell=True, capture_output=True, text=True)
    updates = updates_output.stdout.split('\n')
    # Initialize output
    updates_display = ""
    # Check if we actually got any updates
    if not updates:
        updates_display += "| None!\n"
    else:
        for update in updates:
            # Color updates red if there's an macOS update
            if "macOS" in update:
                updates_display += f"| macOS\n"
            else:
                updates_display += f"| {update}\n"
    return updates_display
# System Sharing Name
system_sharing_name_label = tk.Label(root, text="System Sharing Name:")
system_sharing_name_label.grid(row=0, column=0, sticky="w",padx=10)
system_sharing_name_text = tk.StringVar()
system_sharing_name_entry = tk.Entry(root, textvariable=system_sharing_name_text, state="readonly")
system_sharing_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
# In Active Directory?
in_ad_label = tk.Label(root, text="Active Directory:")
in_ad_label.grid(row=1, column=0, sticky="w",padx=10)
in_ad_text = tk.StringVar()
in_ad_entry = tk.Entry(root, textvariable=in_ad_text, state="readonly", width=20)
in_ad_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
# Host Name
host_name_label = tk.Label(root, text="Host Name:")
host_name_label.grid(row=2, column=0, sticky="w",padx=10)
host_name_text = tk.StringVar()
host_name_entry = tk.Entry(root, textvariable=host_name_text, state="readonly")
host_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
# LAPS Status
laps_status_label = tk.Label(root, text="LAPS Status:")
laps_status_label.grid(row=3, column=0, sticky="w",padx=10)
laps_status_text = tk.StringVar()
laps_status_entry = tk.Entry(root, textvariable=laps_status_text, state="readonly")
laps_status_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
# Admin Users
admin_users_label = tk.Label(root, text="Admin Users:")
admin_users_label.grid(row=4, column=0, sticky="w",padx=10)
# Get admin users' output
admin_users_output = get_admin_users()
# Create a ScrolledText widget to display admin users
admin_users_text = scrolledtext.ScrolledText(root, width=40, height=5)
admin_users_text.grid(row=4, column=1, padx=10, pady=5, sticky="w")
# Insert the admin users' output into the ScrolledText widget
admin_users_text.insert(tk.END, admin_users_output)
# Disable editing of the ScrolledText widget
admin_users_text.configure(state="disabled")
# ATP Check
atp_check_label = tk.Label(root, text="ATP Check:")
atp_check_label.grid(row=5, column=0, sticky="w",padx=10)
atp_status_text = tk.StringVar()
atp_status_entry = tk.Entry(root, textvariable=atp_status_text, state="readonly", width=23)
atp_status_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
# Available System Updates
updates_label = tk.Label(root, text="System Updates:")
updates_label.grid(row=6, column=0, sticky="w",padx=10)
updates_text = tk.StringVar()
# Create a scrolledtext widget for displaying system updates
updates_scrollbar = tk.Scrollbar(root, orient="vertical")
updates_textbox = scrolledtext.ScrolledText(root, state="disabled", width=40, height=5, wrap="word")
updates_textbox.grid(row=6, column=1, padx=10, pady=5, sticky="w")
 
 
# Refresh Button
refresh_button = tk.Button(root, text="Refresh", command=update_components)
refresh_button.grid(row=15, column=2, columnspan=5, padx=10, pady=10)
# Initial update of components
update_components()
def admins():
    try:
        subprocess.run(["osascript", "-e", "do shell script \"sudo /usr/local/bin/jamf policy -trigger addAdmin\" with administrator privileges"])
    except subprocess.CalledProcessError:
        print("Error: Failed to execute addAdmins-loading.sh.")
    except Exception as e:
        print(f"Unexpected error: {e}")
def button_click():
    # Call the admins function when the button is clicked
    admins()
# Create a button to trigger the admins function
button = tk.Button(root, text="Add Admins", command=button_click)
button.grid(row=4, column=3, padx=10, pady=10)  # Use grid to place the button
def update():
    try:
        # Open the System Preferences
        subprocess.run(["open", "-a", "System Preferences"])
        time.sleep(1)  # Wait for the System Preferences to open
        # Click on the General settings
        subprocess.run(["osascript", "-e", 'tell application "System Preferences" to reveal anchor "General" of pane id "com.apple.preference.general"'])
        subprocess.run(["osascript", "-e", 'tell application "System Preferences" to activate'])
        time.sleep(1)  # Wait for the General settings to load
        # Click on the Software Update button
        subprocess.run(["osascript", "-e", 'tell application "System Events" to tell process "System Preferences" to click button 2 of group 1 of scroll area 1 of group 1 of group 2 of splitter group 1 of window 1'])
    except Exception as e:
        print(f"An error occurred: {e}")
 
 
# Create the update button
update_button = tk.Button(root, text="Update", command=update)
update_button.grid(row=6, column=3, padx=10, pady=10)
def run_jamf_recon_policy():
    try:
        # Run jamf recon with administrator privileges
        subprocess.run(["osascript", "-e", 'do shell script "sudo /usr/local/bin/jamf recon" with administrator privileges'])
        # Run jamf policy with administrator privileges
        subprocess.run(["osascript", "-e", 'do shell script "sudo /usr/local/bin/jamf policy" with administrator privileges'])
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
# Create the button to run jamf and recon policy
run_button = tk.Button(root, text="Run jamf and recon policy", command=run_jamf_recon_policy)
run_button.grid(row=15, column=1, padx=10, pady=10)
def defender(baseActionChoices):
    try:
        # Open Microsoft Defender
        subprocess.run(["open", "-a", "Microsoft Defender"])
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        # If there's an error opening Microsoft Defender, display a dialog
        messagebox.showinfo("Microsoft Defender Not Installed", "Microsoft Defender is not installed. The jamf commands are either still running or need to be run. Please wait for it to be installed")
# Create the button to run the Defender function
defender_button = tk.Button(root, text="Microsoft Defender", command=lambda: defender(None))
defender_button.grid(row=15, column=0, padx=10, pady=10)
def cisco(baseActionChoices):
    try:
        # Open Cisco Secure Client
        subprocess.run(["open", "-a", "Cisco Secure Client"])
        # Set Cisco Secure Client to the front
        subprocess.run(["osascript", "-e", 'tell application "System Events" to tell process "Cisco Secure Client" to set frontmost to true'])
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        # If there's an error opening Cisco Secure Client, display a dialog
        messagebox.showinfo("Cisco Secure Client Not Installed", "Cisco Secure Client is not installed. The jamf commands are either still running or need to be run. Please wait for it to be installed")
# Create the button to run the Cisco function
cisco_button = tk.Button(root, text="Run Cisco Secure Client", command=lambda: cisco(None))
cisco_button.grid(row=14, column=1, padx=10, pady=10)
def open_safari_with_url(url):
    try:
        # Open Safari and navigate to the URL
        subprocess.run(["open", "-a", "Safari", url])
        time.sleep(2)  # Wait for Safari to open and load the page
        # Set Safari to the front
        subprocess.run(["osascript", "-e", 'tell application "System Events" to tell application process "Safari" to set frontmost to true'])
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        # If Safari is not installed or encountered an error, display a dialog
        messagebox.showinfo("Error", "Safari is not installed or encountered an error.")
def bomgar():
    try:
        # Open remote.nau.edu in Safari
        open_safari_with_url("https://remote.nau.edu")
        # Call the commands function with baseActionChoices
        # commands(baseActionChoices)  # Uncomment and replace with your actual commands function
    except Exception as e:
        print(f"An error occurred in bomgar function: {e}")
        # You can also display a messagebox here if needed
# Create the button to run the Bomgar function
bomgar_button = tk.Button(root, text="Test Bomgar", command=bomgar)
bomgar_button.grid(row=13, column=1, pady=10)
def get_wifi_information():
    model_process = subprocess.run(["system_profiler", "SPHardwareDataType"], capture_output=True, text=True)
    model_output = model_process.stdout
    model = [line.split(":")[1].strip() for line in model_output.splitlines() if "Model Name" in line]
    available_wifi_process = subprocess.run(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport", "-s"], capture_output=True, text=True)
    available_wifi = available_wifi_process.stdout
    connected_wifi_process = subprocess.run(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport", "-I"], capture_output=True, text=True)
    connected_wifi = connected_wifi_process.stdout
    wifi_result = ""
    wifi_check = "0"
    if "MacBook" in model:
        if "NAU" in available_wifi:
            if "NAU" in connected_wifi and "running" in connected_wifi:
                wifi_result = "Laptop is connected to NAU wifi"
                wifi_check = "1"
            else:
                wifi_result = "Laptop needs to be connected to NAU wifi"
        else:
            wifi_result = "Laptop cannot detect NAU wifi"
    else:
        wifi_result = "Wifi connection optional"
        wifi_check = "1"
    return wifi_result
# Create and place the label using grid
wifi_label = tk.Label(root, text="Wifi Information:")
wifi_label.grid(row=12, column=0, sticky="w",padx=10)  
# Get wifi information
wifi_info = get_wifi_information()
# Create and place the entry widget using grid
wifi_entry = tk.Entry(root, width=30)
wifi_entry.insert(tk.END, wifi_info)  # Insert wifi information into the entry widget
wifi_entry.grid(row=12, column=1, padx=10, pady=10)  # Add padding for better appearance
# Create and place the label using grid
bomgar_label = tk.Label(root, text="BOMGAR status:")
bomgar_label.grid(row=13, column=0, sticky="w",padx=10)
# Create and place the label using grid
cisco_label = tk.Label(root, text="CISCO status:")
cisco_label.grid(row=14, column=0, sticky="w",padx=10)
#Start the GUI
root.mainloop()
