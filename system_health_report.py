import psutil
import webbrowser
import os
import subprocess
from datetime import datetime

# Function to fetch disk health
def get_disk_health_html():
    disks = [disk for disk in psutil.disk_partitions(all=False) if disk.fstype != ""]
    disk_html = "<table><tr><th>Device</th><th>Mountpoint</th><th>Filesystem</th><th>Total Size (GB)</th><th>Used (GB)</th><th>Free (GB)</th><th>Usage (%)</th></tr>"
    for disk in disks:
        usage = psutil.disk_usage(disk.mountpoint)
        disk_html += f"<tr><td>{disk.device}</td><td>{disk.mountpoint}</td><td>{disk.fstype}</td><td>{usage.total / (1024 ** 3):.2f}</td><td>{usage.used / (1024 ** 3):.2f}</td><td>{usage.free / (1024 ** 3):.2f}</td><td>{usage.percent}%</td></tr>"
    disk_html += "</table>"
    return disk_html

# Function to fetch battery status and health
def get_battery_status_html():
    battery = psutil.sensors_battery()
    if battery:
        battery_html = f"""<table>
<tr><th>Plugged In</th><th>Charge (%)</th><th>Battery Left (hrs)</th></tr>
<tr><td>{battery.power_plugged}</td><td>{battery.percent}%</td><td>{battery.secsleft / 3600:.2f} hrs</td></tr>
</table>"""
    else:
        battery_html = "<p>No battery detected</p>"
    return battery_html

# Function to get installed software details on Windows
def get_installed_software_html():
    # Adjusted command for simpler parsing: outputting as CSV
    cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-Command",
           "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*, "
           "HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | "
           "Where-Object { $_.DisplayName -ne $null } | "
           "Select-Object DisplayName, DisplayVersion, InstallDate | "
           "ConvertTo-Csv -NoTypeInformation"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        lines = result.stdout.split('\n')
        software_html = "<table id='softwareTable'><thead><tr><th>Name</th><th>Version</th><th>Installation Date</th></tr></thead><tbody>"
        
        # Skip the CSV header
        for line in lines[1:]:
            if line.strip():
                parts = line.strip().split(',')
                # Cleanup and format each part
                name = parts[0].strip('"')
                version = parts[1].strip('"')
                # Convert and format the installation date if available
                install_date = parts[2].strip('"')
                if install_date:
                    # Assuming the InstallDate format is YYYYMMDD
                    install_date = datetime.strptime(install_date, '%Y%m%d').strftime('%d/%m/%Y') if install_date else 'Unknown'
                software_html += f"<tr><td>{name}</td><td>{version}</td><td>{install_date}</td></tr>"
                
        software_html += "</tbody></table>"
        return software_html
    except Exception as e:
        return f"<p>Error fetching software information: {str(e)}</p>"



# Include DataTables initialization in your HTML template
def generate_html_report():
    disk_health_html = get_disk_health_html()
    battery_status_html = get_battery_status_html()
    software_html = get_installed_software_html()
    
    html_content = f"""
    <html>
    <head>
        <title>System Health Report - {datetime.now().strftime('%Y-%m-%d')}</title>
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.25/css/jquery.dataTables.css">
        <script type="text/javascript" src="https://code.jquery.com/jquery-3.5.1.js"></script>
        <script type="text/javascript" src="https://cdn.datatables.net/1.10.25/js/jquery.dataTables.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            td, th {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            h2 {{ color: #4CAF50; }}
        </style>
        <script>
            $(document).ready(function() {{
                $('#softwareTable').DataTable();
            }});
        </script>
    </head>
    <body>
        <h2>Disk Health</h2>
        {disk_health_html}
        <h2>Battery Status</h2>
        {battery_status_html}
        <h2>Installed Software</h2>
        {software_html}
    </body>
    </html>
    """
    
    filename = "system_health_report.html"
    with open(filename, "w") as f:
        f.write(html_content)
    
    webbrowser.open(f"file://{os.path.realpath(filename)}")

# Execute the script
if __name__ == "__main__":
    generate_html_report()
