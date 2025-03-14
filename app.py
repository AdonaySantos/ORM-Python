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

@app.route('/insert/<string:table_name>', methods=['POST'])
def insert_data(table_name):
    if not request.is_json:
        return jsonify({"error" : "A requisição deve ser em formato JSON"}), 400
    
    columns = request.json.get("columns")
    data = request.json.get("data")
    
    if not columns:
        return jsonify({"error" : "Nenhuma coluna especificada"}), 400
    return table_service.insert_data(table_name, columns, data)

@app.route('/delete/<string:table_name>', methods=['DELETE'])
def delete_data(table_name):
    if not request.is_json:
        return jsonify({"error" : "A requisição deve ser em formato JSON"}), 400
    
    conditions = request.json.get("conditions")
    
    if not conditions:
        return jsonify({"error" : "Nenhuma condição especificada"}), 400
    return table_service.delete_data(table_name, conditions)

@app.route('/update/<string:table_name>', methods=["PUT"])
def update_data(table_name):
    if not request.is_json:
        return jsonify({"error" : "A requisição deve ser em formato JSON"}), 400
    
    conditions = request.json.get("conditions")
    new_values = request.json.get("values")
    
    if not conditions or not new_values:
        return jsonify({"error" : "Nenhuma condição especificada ou nenhum dado novo"}), 400
    
    if not isinstance(new_values, dict):
        return jsonify({"error" : "'values' deve ser um dicionário com colunas e novos valores"}), 400

    return table_service.update_data(table_name, conditions, new_values)

if __name__ == "__main__":
    app.run(debug=True)