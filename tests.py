from ORM import DB_ORM
import json

db = DB_ORM()

db.get_connection()

print(db.get_tables())

table_departamentos = db.get_table_schema("departamentos")
table_funcionarios = db.get_table_schema("funcionarios")

print(json.dumps(table_departamentos, indent=4, ensure_ascii=False))
print(json.dumps(table_funcionarios, indent=4, ensure_ascii=False))
