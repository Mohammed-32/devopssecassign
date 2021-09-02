import json
import requests
import urllib
from urllib.request import urlopen
json_url = urlopen('http://aed7b0d3094294f45ac8057e1bb75e87-1543800842.us-east-2.elb.amazonaws.com:8080/getStatus')
data = json.loads(json_url.read())
print(data) 
