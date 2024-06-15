import requests
import json

response = requests.get('http://ipinfo.io/json')
data = response.json()
city = data['city']
print(city)
def decimal_to_dms(decimal):
    degrees = int(decimal)
    minutes = int((decimal - degrees) * 60)
    seconds = (decimal - degrees - minutes / 60) * 3600
    return degrees, minutes, seconds

def format_dms(degrees, minutes, seconds, direction):
    return f"{degrees}°{minutes}'{seconds:.1f}\"{direction}"

# Get location data from ipinfo.io
response = requests.get('http://ipinfo.io/json')
data = response.json()

# Extract latitude and longitude
latitude, longitude = map(float, data['loc'].split(','))

# Convert latitude to DMS
lat_degrees, lat_minutes, lat_seconds = decimal_to_dms(abs(latitude))
lat_direction = 'N' if latitude >= 0 else 'S'

# Convert longitude to DMS
long_degrees, long_minutes, long_seconds = decimal_to_dms(abs(longitude))
long_direction = 'E' if longitude >= 0 else 'W'

# Format the coordinates
formatted_lat = format_dms(lat_degrees, lat_minutes, lat_seconds, lat_direction)
formatted_long = format_dms(long_degrees, long_minutes, long_seconds, long_direction)

# Print the formatted coordinates
print(f"{formatted_lat} {formatted_long}")

