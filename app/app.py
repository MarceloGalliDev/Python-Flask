from flask import Flask, Response, g, request
import sqlite3

app = Flask(__name__)
DB_URL = 'enterprise.db'

users = [
  {
    "username": "marcelo", "password": "admin123admin"
  }
]

#esse decorator diz que quando for inicializar o servido sera a primeira função a ser executada
@app.before_request
def before_request():
  print('Conectando ao banco')
  conn = sqlite3.connect(DB_URL)
  g.conn = conn
  
  
#usando quando temos erro e sucesso na requisição, e para fechameto da conexão
#sempre é executada após uma requisição, não precisamos dar o comando de fechamento
@app.teardown_request
def after_request(exception):
  if g.conn is not None:
    g.conn.close()
    print('Desconectando ao banco')


#função de validação simples
def check_user(username, password):
  for user in users:
    if (user['username'] == username) and (user['password'] == password):
      return True
  return False


@app.route('/empregados')
def get_empregados():
  
  query = '''
    SELECT nome, cargo, salario
    FROM empregados;
  '''

  cursor = g.conn.execute(query)
  #list compreension
  employees_dict = [
    {
      'nome':row[0], 
      'cargo':row[1],
      'salaio':row[2]
    }
    for row in cursor.fetchall()
  ]
  print(employees_dict)
  
  return {'empregados':employees_dict}

@app.route('/')
def hello():
  return '<h1>Hello World!</h1>'

# @app.route('/empregados/<cargo>')
# def get_empregados_cargo(cargo):
#   out_empregados = []
#   for empregado in empregados:
#     if cargo == empregado['cargo'].lower():
#       out_empregados.append(empregado)
#   return {'empregados': out_empregados}
  
  
# @app.route('/empregados/<info>/<value>')
# def get_empregados_info(info, value):
#   out_empregados = []
#   for empregado in empregados:
#     if info in empregado.keys():
#       value_empregado = empregado[info]
      
#       if type(value_empregado) == str:
#         if value == value_empregado.lower():
#           out_empregados.append(empregado)
      
#       if type(value_empregado) == int:
#         if int(value) == value_empregado:
#           out_empregados.append(empregado)
#   return {'empregados': out_empregados}


# @app.route('/informations', methods=['POST'])
# def post_empregados():
  
#   username = request.form['username']
#   password = request.form['password']
  
#   if not check_user(username, password):
#     return Response('Unauthorized', status=401)
  
#   info = request.form['info']
#   value = request.form['value']
  
  
#   out_empregados = []
#   for empregado in empregados:
#     if info in empregado.keys():
#       value_empregado = empregado[info]
      
#       if type(value_empregado) == str:
#         if value == value_empregado.lower():
#           out_empregados.append(empregado)
      
#       if type(value_empregado) == int:
#         if int(value) == value_empregado:
#           out_empregados.append(empregado)
#   return {'empregados': out_empregados}
  
  
if __name__ == '__main__':
  app.run(debug=True)