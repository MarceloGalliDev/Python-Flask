import requests

# method GET
get_response = requests.get('http://127.0.0.1:5000/empregados/cargo/analista')

get_message = get_response.json()

print(get_response.text)
print(type(get_response.text))
print(get_message['empregados'])

get_response_empregados = requests.get('http://127.0.0.1:5000/empregados')


#----------------------------------------------------------------

# method POST
data = {
  "username": "Marcelo", 
  "password":"admin123admin", 
  "info": "cargo", 
  "value": "analista"
}

post_response = requests.post('http://127.0.0.1:5000/informations', data=data)


if post_response.status_code == 200:
  post_message = post_response.json()
  print(post_message['empregados'])
else:
  print(post_response.status_code)