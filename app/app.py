from flask import Flask, Response, g, request
import sqlite3

app = Flask(__name__)
DB_URL = 'app/enterprise.db'

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
#----------------------------------------------------------------

  
#usando quando temos erro e sucesso na requisição, e para fechameto da conexão
#sempre é executada após uma requisição, não precisamos dar o comando de fechamento
@app.teardown_request
def after_request(exception):
  if g.conn is not None:
    g.conn.close()
    print('Desconectando ao banco')
#----------------------------------------------------------------


#função de validação simples
def check_user(username, password):
  for user in users:
    if (user['username'] == username) and (user['password'] == password):
      return True
  return False
#----------------------------------------------------------------


#estamos transformando os dados em formato JSON
def query_employers_to_dict(conn, query):
  cursor = conn.cursor()
  cursor.execute(query)
  
  employees_dict = [
    {
      'nome':row[0],
      'cargo':row[1],
      'salario':row[2]
    }
    for row in cursor.fetchall()
  ]
  
  return employees_dict
#----------------------------------------------------------------


#rota empregados
@app.route('/empregados')
def get_empregados():
  
  query = '''
    SELECT nome, cargo, salario
    FROM empregados;
  '''
  
  employees_dict = query_employers_to_dict(g.conn, query)
  
  return {'empregados':employees_dict}
#----------------------------------------------------------------


#rota home
@app.route('/')
def hello():
  return '<h1>Hello World!</h1>'
#----------------------------------------------------------------


#rota empregados/cargo
@app.route('/empregados/<cargo>')
def get_empregados_cargo(cargo):
  query = '''
    SELECT nome, cargo, salario
    FROM empregados
    WHERE "cargo" LIKE "{}";
  '''.format(cargo)
  
  employees_dict = query_employers_to_dict(g.conn, query)
  
  return {'empregados': employees_dict}
#----------------------------------------------------------------
 

#rota empregados/info/value  
@app.route('/empregados/<info>/<value>')
def get_empregados_info(info, value):
  if value.isnumeric():
    value = float(value)
    
  query = '''
    SELECT nome, cargo, salario
    FROM empregados
    WHERE "{}" LIKE "{}";
  '''.format(info, value)
  
  employees_dict = query_employers_to_dict(g.conn, query)
  
  return {'empregados': employees_dict}
#----------------------------------------------------------------


@app.route('/informations', methods=['POST'])
def post_empregados():
  
  username = request.form['username']
  password = request.form['password']
  
  if not check_user(username, password):
    return Response('Unauthorized', status=401)
  
  info = request.form['info']
  value = request.form['value']
  
  if value.isnumeric():
    value = float(value)
    
  query = '''
    SELECT nome, cargo, salario
    FROM empregados
    WHERE "{}" LIKE "{}";
  '''.format(info, value)
  
  employees_dict = query_employers_to_dict(g.conn, query)
  
  return {'empregados': employees_dict}


@app.route('/register', methods=['POST'])
def post_empregados_cadastro():
  
  # username = request.form['username']
  # password = request.form['password']
  
  # if not check_user(username, password):
  #   return Response('Unauthorized', status=401)
  
  nome = request.form.get('nome')
  cargo = request.form.get('cargo')
  salario = request.form.get('salario')

  query = '''
    INSERT INTO empregados (nome, cargo, salario)
    VALUES ("{}", "{}", "{}");
  '''.format(nome, cargo, salario)
  
  cursor = g.conn.cursor()
  cursor.execute(query)
  
  g.conn.commit()
  
  
  return {'empregados': 'Registered employee'}
  
  
if __name__ == '__main__':
  app.run(debug=True)