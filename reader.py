# import urllib library
from urllib.request import urlopen
  
# import json
import json
# store the URL in url as 
# parameter for urlopen
url = "http://127.0.0.1:5000"
  
# store the response of URL
while(True):
    response = urlopen(url)
    
    # storing the JSON response 
    # from url in data
    data_json = json.loads(response.read())
    
    # print the json response
    if(len(data_json)>0):
        print(data_json)
