import requests 
  
# api-endpoint 
URL = "http://127.0.0.1:5000/"
  
# defining a params dict for the parameters to be sent to the API 
PARAMS = {"base64":"asrgwetrgvsefdv"} 
  
# sending get request and saving the response as response object 
r = requests.get("http://127.0.0.1:5000/",json={'base64': 'wergwergvertger'})
# breakpoint()
  
# extracting data in json format 
data = r.json() 
print(data)