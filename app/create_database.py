import sqlite3

conn = sqlite3.connect('app/enterprise.db')

#cursor é responsavel pela interface do banco de dados
cursor = conn.cursor()

cursor.execute("""
  CREATE TABLE IF NOT EXISTS empregados (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cargo TEXT NOT NULL,
    salario REAL NOT NULL    
  );
""")

print('Tabela criada com sucesso!')

#desconect do banco de dados
conn.close()
