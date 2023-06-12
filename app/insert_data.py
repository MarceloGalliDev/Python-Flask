import sqlite3

empregados = [
  {'nome':'Marcelo', 'cargo':'Engenheiro', 'salario': 5000},
  {'nome':'Gustavo', 'cargo':'Analista', 'salario': 3000},
  {'nome':'Vitor', 'cargo':'Marketing', 'salario': 3000},
  {'nome':'Luiz', 'cargo':'Assistente', 'salario': 2000}
]

conn = sqlite3.connect('enterprise.db')

cursor = conn.cursor()

for empregado in empregados:
  cursor.execute("""
    INSERT INTO empregados (nome, cargo, salario)
    VALUES (?,?,?)
  """, (
    empregado['nome'], 
    empregado['cargo'], 
    empregado['salario']
  ))

print('Dados salvos!')

#salve dos dados
conn.commit()

#fechamento da conexão
conn.close()
