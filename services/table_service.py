from models.db_orm import DBORM
from flask import jsonify

class TableService:
    def __init__(self):
        self.db = DBORM()
        
    def get_tables(self):
        result = self.db.execute_query("SHOW TABLES")
        
        if isinstance(result, list):
            return [table[0] for table in result]
        return result
    
    def get_table_schema(self, table_name: str):
        result = self.db.execute_query(f"SHOW COLUMNS FROM {table_name}")
        
        if isinstance(result, list):
            return {
                column[0]: {
                    "Tipo": column[1],   
                    "Null": column[2],   
                    "Key": column[3],   
                    "Default": column[4],   
                    "Extra": column[5]   
                }
                for column in result
            }
        return result
    
    def get_data(self, table_name: str, columns: list[str]):
        query = f"SELECT {", ".join(columns)} FROM {table_name}"
        result = self.db.execute_query(query)
        
        if not isinstance(result, list):
            return result
        
        data = []
        for row in result:
            row_dict = {columns[i]: row[i] for i in range(len(columns))}
            data.append(row_dict)
            
        return jsonify(data)
    
    def insert_data(self, table_name: str, columns: list[str], data: list[str]):
        if not data:
            return jsonify({"error" : "Nenhum dado fornecido"}), 400
        
        clmns = ", ".join(columns)
        dta = ", ".join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({clmns}) VALUES ({dta})"
        values = tuple(data)
        
        try:
            result = self.db.execute_query(query, fetch=False, values=values)
            return jsonify({"message" : "Registro inserido com sucesso", "id" : result})
        except Exception as e:
            return jsonify({"error" : f"{e}"}), 500
            
    def delete_data(self, table_name: str, conditions: list[str]):
        if len(conditions) > 1:
            conditions = " AND ".join(conditions)
        
        query = f"DELETE FROM {table_name} WHERE {conditions}"
        
        try:
            result = self.db.execute_query(query, fetch=False)
            return jsonify({"message" : "Registro deletado com sucesso"})
        except Exception as e:
            return jsonify({"error" : f"{e}"}), 500
        