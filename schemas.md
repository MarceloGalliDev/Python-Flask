# Schemas
> Usados para serializar os dados, de como serão apresentados
> Usados para transformar os dados do tipo json para py e ao contrário também

## Exemplos
'''
response = requests.get('http://localhost:5000/empregados/cargo/analista')

message = response.json

print(response)
print(response.text)
print(type(response.text))
print(message)
'''

### Inserção de dados

empregados = [
  {'nome':'Marcelo', 'cargo':'Engenheiro_de_Software', 'salario': 5000},
  {'nome':'Gustavo', 'cargo':'Analista', 'salario': 5000},
  {'nome':'Vitor', 'cargo':'Marketeiro', 'salario': 3000},
]

conn = sqlite3.connect('{nome_banco}.db')

cursor - conn.cursor()

for empregado in empregados:
  cursor.execute("""
    INSERT INTO empregados (nome, cargo, salario)
    VALUES (?, ?, ?)
  """, (empregado['nome'], empregado['cargo'], empregado['salario']))

print('Dados inseridos com sucesso!')

conn.commit()
conn.close()