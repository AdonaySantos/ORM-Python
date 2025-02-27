from ORM import ORM

bd = ORM()

bd.get_connection()

print(bd.get_tables())
