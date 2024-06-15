import urllib3
import json
http = urllib3.PoolManager()
r = http.request('GET', 'http://ipinfo.io/json')
data = json.loads(r.data.decode('utf-8'))
city=data['city']
loc=data['loc']
print(city,loc)
