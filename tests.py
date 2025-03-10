from ORM import DB_ORM
import json

db = DB_ORM()

db.get_connection()

print(db.get_tables())

table_departamentos = db.get_table_schema("departamentos")
table_funcionarios = db.get_table_schema("funcionarios")

print(json.dumps(table_departamentos, indent=4, ensure_ascii=False))
print(json.dumps(table_funcionarios, indent=4, ensure_ascii=False))

data_departamentos = db.get_data("departamentos", ["id_departamento", "nome_departamento"])
data_funcionarios = db.get_data("funcionarios", ["id_funcionario", "nome_funcionario", "id_departamento"])

print(data_departamentos)
print()
print(data_funcionarios)
