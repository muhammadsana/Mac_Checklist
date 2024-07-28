Mac Computer Information and Status GUI

This is a Python application with a graphical user interface (GUI) built using Tkinter. The application retrieves and displays various system information and statuses for a macOS computer.

Features
- System Sharing Name: Retrieves and displays the macOS system sharing name.
- Active Directory Status: Checks if the host is bound to an Active Directory domain.
- Host Name: Retrieves and displays the macOS host name.
- LAPS Status: Checks and displays the status of Local Administrator Password Solution (LAPS).
- Admin Users: Lists all administrative users on the system.
- ATP Check: Checks and displays the status of Microsoft Defender Advanced Threat Protection (ATP).
- System Updates: Displays available system updates.
- Admin Management: Adds administrative users.
- System Preferences Update: Opens System Preferences and navigates to Software Update.
- Jamf Management: Runs Jamf recon and policy commands with administrator privileges.
- Microsoft Defender: Opens Microsoft Defender.
- Cisco Secure Client: Opens Cisco Secure Client.
- Safari URL: Opens Safari and navigates to a specified URL.
- Bomgar Test: Opens the remote.nau.edu URL in Safari.
- WiFi Information: Retrieves and displays WiFi connection information.

Installation
Ensure you have Python 3 installed.
Install the required libraries:
bash
Copy code
pip install tk

Usage
Clone this repository to your local machine.
Navigate to the directory containing the script.

Run the script:
bash
Copy code

Script Overview

GUI Components
Labels and Entries: Display system information such as system sharing name, Active Directory status, host name, LAPS status, ATP status, and WiFi information.
ScrolledText: Displays the list of admin users and available system updates.
Buttons: Provide functionality to refresh data, add admins, open System Preferences, run Jamf commands, open Microsoft Defender, run Cisco Secure Client, and test Bomgar.

Functions
update_components: Refreshes all the displayed components with the latest system information.
get_system_sharing_name: Retrieves the macOS system sharing name using scutil.
get_host_name: Retrieves the macOS host name using hostname.
check_laps_status: Checks the status of LAPS using log files.
is_bound_to_active_directory: Checks if the host is bound to an Active Directory domain using dsconfigad.
get_admin_users: Retrieves the list of admin users using dscl.
check_atp: Checks the status of ATP using mdatp.
display_system_updates: Retrieves and displays available system updates using softwareupdate.
admins: Adds administrative users by running a Jamf policy.
update: Opens System Preferences and navigates to Software Update.
run_jamf_recon_policy: Runs Jamf recon and policy commands.
defender: Opens Microsoft Defender.
cisco: Opens Cisco Secure Client.
open_safari_with_url: Opens Safari and navigates to a specified URL.
bomgar: Opens the remote.nau.edu URL in Safari.
get_wifi_information: Retrieves and displays WiFi connection information.

Notes
This script uses subprocess to run various macOS commands and retrieve system information.
Some functions require administrator privileges and may prompt for the admin password.
