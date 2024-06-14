import time
import psutil
import ctypes
import logging
from time import sleep
from logging.handlers import RotatingFileHandler
import urllib.request
import wmi

# Setup enhanced logging with rotation
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_file = 'system_monitor.log'
# Use RotatingFileHandler for log rotation (5 MB max per log file, keep up to 5 old log files)
handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024, backupCount=5, encoding=None, delay=0)
handler.setFormatter(log_formatter)
handler.setLevel(logging.INFO)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Function to check for high CPU usage
def check_cpu_usage(threshold=75):
    return psutil.cpu_percent(interval=1) > threshold

# Function to check battery status
def check_battery_status(low_battery_threshold=20):
    battery = psutil.sensors_battery()
    if battery:
        return battery.percent <= low_battery_threshold
    return False

# Check disk usage
def check_disk_usage(threshold=75):
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        if usage.percent >= threshold:
            return True, partition.mountpoint
    return False, None

# Check memory usage
def check_memory_usage(threshold=80):
    memory = psutil.virtual_memory()
    return memory.percent >= threshold

# Network usage check placeholder
def check_network_usage(threshold=1000 * 1024 * 1024):  # Threshold in bytes (e.g., 1000MB)
    # Get network stats at start
    net1 = psutil.net_io_counters()
    sleep(1)  # Measure over 1 second
    # Get network stats after 1 second
    net2 = psutil.net_io_counters()
    # Calculate bytes sent/received during this period
    bytes_sent = net2.bytes_sent - net1.bytes_sent
    bytes_recv = net2.bytes_recv - net1.bytes_recv

    # Check if the total bytes sent/received exceeds the threshold
    if (bytes_sent + bytes_recv) >= threshold:
        return True
    return False

# Check CPU temperature - This function is a placeholder. Actual implementation depends on specific libraries like `psutil.sensors_temperatures()` which may not be available on all systems.
def check_temperature_wmi(threshold=75):
    w = wmi.WMI(namespace="root\wmi")
    temperature_info = w.MSAcpi_ThermalZoneTemperature()
    for sensor in temperature_info:
        # Convert from tenths of Kelvin to Celsius
        temp_celsius = (sensor.CurrentTemperature / 10.0) - 273.15
        if temp_celsius >= threshold:
            return True
    return False

# Check process resource usage
def check_process_resource_usage(process_name, cpu_threshold=10, memory_threshold=100*1024*1024):  # CPU % and memory in bytes
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        if proc.info['name'] == process_name:
            cpu_usage = proc.info['cpu_percent']
            memory_usage = proc.info['memory_info'].rss  # Resident Set Size
            if cpu_usage > cpu_threshold or memory_usage > memory_threshold:
                return True, cpu_usage, memory_usage
    return False, 0, 0

# Check system uptime
def check_system_uptime(max_uptime_hours=24):
    uptime_seconds = time.time() - psutil.boot_time()
    return uptime_seconds / 3600 > max_uptime_hours

# Check internet connection
def check_internet_connection(url='http://www.google.com'):
    try:
        urllib.request.urlopen(url, timeout=10)
        return True
    except urllib.error.URLError:
        return False
    
# Function to display a custom Windows alert
def show_windows_alert(title, message):
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, message, title, 0x40 | 0x0)

# Main loop to continuously check for conditions
while True:
    # Disk usage
    disk_usage_exceeded, partition = check_disk_usage()
    if disk_usage_exceeded:
        message = f"Disk usage on partition {partition} is high. Consider cleaning up."
        logger.warning(message)  # Using warning level as an example
        show_windows_alert("Disk Usage Alert", message)
    
    # Memory usage
    if check_memory_usage():
        message = "Memory usage is high. Consider closing some applications."
        logger.warning(message)  # Adjusting log level as needed
        show_windows_alert("Memory Usage Alert", message)
    
    # CPU usage
    if check_cpu_usage():
        message = "CPU usage is high. Consider closing some applications."
        logger.info(message)  # Info level for regular alerts
        show_windows_alert("High CPU Usage Alert", message)
    
    # Battery status
    if check_battery_status():
        message = "Battery level is low. Consider plugging in your device."
        logger.info(message)  # Info level for regular alerts
        show_windows_alert("Low Battery Alert", message)
    
    # Network usage
    if check_network_usage():
        message = "High network usage detected. This might affect your internet speed."
        logger.warning(message)
        show_windows_alert("High Network Usage Alert", message)

    # CPU temperature
    if check_temperature_wmi():
        message = "High CPU temperature detected. Consider checking your cooling system."
        logger.warning(message)
        show_windows_alert("High CPU Temperature Alert", message)

    # Process-specific monitoring
    process_check = check_process_resource_usage('example_process.exe')
    if process_check[0]:
        message = f"Process 'example_process.exe' is using high resources: CPU {process_check[1]}%, Memory {process_check[2]} bytes."
        logger.warning(message)
        show_windows_alert("Process Resource Alert", message)

    # System uptime
    if check_system_uptime():
        message = "System has been running for more than 24 hours."
        logger.info(message)
        show_windows_alert("System Uptime Alert", message)

    # Internet connectivity
    if not check_internet_connection():
        message = "Internet connection appears to be down."
        logger.error(message)
        show_windows_alert("Internet Connectivity Alert", message)

    sleep(60)  # Sleep time can be adjusted as needed
