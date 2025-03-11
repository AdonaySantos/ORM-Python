from flask import Flask, jsonify, request
from services.table_service import TableService

app = Flask(__name__)
table_service = TableService()

@app.route("/tables", methods=['GET'])
def get_tables():
    return jsonify({"tables" : table_service.get_tables()})

@app.route("/schema/<string:table_name>", methods=['GET'])
def get_table_schema(table_name):
    return jsonify(table_service.get_table_schema(table_name))

@app.route("/data/<string:table_name>", methods=['POST'])
def get_data(table_name):
    if not request.is_json:
        return jsonify({"error" : "A requisição deve ser em formato JSON"}), 400
    
    columns = request.json.get("columns")
    
    if not columns:
        return jsonify({"error" : "Nenhuma coluna especificada"}), 400
    return table_service.get_data(table_name, columns)

@app.route('/<string:table_name>', methods=['POST'])
def insert_data(table_name):
    if not request.is_json:
        return jsonify({"error" : "A requisição deve ser em formato JSON"}), 400
    
    columns = request.json.get("columns")
    data = request.json.get("data")
    
    if not columns or not data:
        return jsonify({"error" : "Nenhuma coluna especificada ou nenhum dado inserido"}), 400
    return table_service.insert_data(table_name, columns, data)

if __name__ == "__main__":
    app.run(debug=True)