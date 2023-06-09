from flask import Flask, request
import sqlite3

app = Flask(__name__)

DB_URL = '{nome_banco}.db'

@app.before_request
def before_request():
  print('Conectando ao banco')
  conn = sqlite3.connect(DB_URL)
  g.conn = conn
  
  
#usando quando temos erro e sucesso na requisição
@app.teardown_request
def after_request(exception):
  if g.conn is not None:
    g.conn.close()
    print('Desconectando ao banco')


def query_employers_to_dict(conn, query):
  cursor = g.conn.execute(query)
  
  employees_dict =[
    {
      'nome':row[0],
      'cargo':row[1],
      'salaio':row[2]
    }
    for row in cursor.fetchall()
  ]
  
  return employees_dict

@app.route('/')
def hello():
  return '<h1>Hello World!</h1>'


@app.route('/empregados')
def get_empregados():
  query = '''
    SELECT nome, cargo, salaio
    FROM empregados
  '''
  
  return {'empregados':employees_dict}


@app.route('/empregados/<cargo>')
def get_empregados_cargo(cargo):
  out_empregados = []
  for empregado in empregados:
    if cargo == empregado['cargo'].lower():
      out_empregados.append(empregado)
  return {'empregados': out_empregados}
  
  
@app.route('/empregados/<info>/<value>')
def get_empregados_info(info, value):
  out_empregados = []
  for empregado in empregados:
    if info in empregado.keys():
      value_empregado = empregado[info]
      
      if type(value_empregado) == str:
        if value == value_empregado.lower():
          out_empregados.append(empregado)
      
      if type(value_empregado) == int:
        if int(value) == value_empregado:
          out_empregados.append(empregado)
  return {'empregados': out_empregados}


@app.route('/informations', methods=['POST'])
def post_empregados():
  
  info = request.form['info']
  value = request.form['value']
  
  
  out_empregados = []
  for empregado in empregados:
    if info in empregado.keys():
      value_empregado = empregado[info]
      
      if type(value_empregado) == str:
        if value == value_empregado.lower():
          out_empregados.append(empregado)
      
      if type(value_empregado) == int:
        if int(value) == value_empregado:
          out_empregados.append(empregado)
  return {'empregados': out_empregados}
  
  
if __name__ == '__main__':
  app.run(debug=True)