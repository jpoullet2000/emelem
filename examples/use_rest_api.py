import requests
import json

r = requests.post('http://localhost:8088/login', data=json.dumps({'username':'jbp', 'password':'jbp'}), headers={'content-type': 'application/json'})
res = requests.get('http://localhost:8088/mlmmodelview/models/1', headers={'Authorization': 'OAuth <ACCESS_TOKEN>', 'content-type': 'application/json'})
print(res)




import sys
import requests

URL = 'http://localhost:8088/login'
URL2 = 'http://localhost:8088/mlmmodelview/models/1'

client = requests.session()

# Retrieve the CSRF token first
client.get(URL)  # sets cookie
#csrftoken = client.cookies['csrf']
csrftoken = client.cookies['session']


login_data = dict(username='jbp', password='jbp', csrfmiddlewaretoken=csrftoken, next='/')
r = client.post(URL, data=login_data, headers=dict(Referer=URL))
res = client.post(URL2, data=login_data, headers=dict(Referer=URL))


import requests
auth_url = 'http://localhost:8088/login'
model_url = 'http://localhost:8088/mlmmodelview/models/1'

session = requests.session()
# Access to a custom route to authenticate the client
# I had to write a custom route for this purpose to bypass CSRF issues
session.get(auth_url, json={"username": 'jbp', "password": 'jbp'})
session.get(model_url)


client.get(URL2)
csrftoken = client.cookies['session']
session.get(auth_url, json={"username": 'jbp', "password": 'jbp'})
res  = session.get(model_url)



r = requests.get('http://localhost:8088', auth=('jbp', 'jbp'))
r2 = requests.get('http://localhost:8088/mlmmodelview/models/1', auth=('jbp', 'jbp'))
res = client.get(URL2, headers=dict(Referer=URL))


curl -i --data 'userName=jbp&password=jbp&csrf_token=IjZlNDFkZGRmZTc3ODE4NjZjMTY2NTVlMGFjN2E4NzQ0OTUwNTI1OTUi.DDaFaQ.ldCOL3hmVvWLnzrjxQxoAzKXtew' -X POST "http://localhost:8088/login/"

curl -v -c cookies.txt -b cookies.txt -d 'username=jbp&password=jbp&csrfmiddlewaretoken
