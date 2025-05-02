"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

miembros_iniciales =[
    {"first_name": "Jhon", "age": 33, "lucky_number":[7,13,22]},
    {"first_name": "Jane", "age": 35, "lucky_number":[10,14,3]},
    {"first_name": "Jimmy", "age": 5, "lucky_number":[1]}
]

for member in miembros_iniciales:
    jackson_family.add_member(member)

 


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    try:
        members = jackson_family.get_all_members()
        response_body = {
                     "family": members}
        return jsonify(response_body), 200

    except Exception:
        response_body = {
            "error" : "Error al recuperar los miembros de la familia"
        }
        return jsonify(response_body), 500


@app.route('/members', methods=['POST'])
def añadir_miembro():
    # This is how you can use the Family datastructure by calling its methods
    try:
        member = request.json
        nuevo_miembro = jackson_family.add_member(member)
        response_body = {
                     "family": nuevo_miembro}
        return jsonify(response_body), 201
    except Exception:
        response_body = {
            "error" : "Error añandiendo un miembro a la familia"
        }
        return jsonify(response_body), 500

@app.route('/members/<int:id>', methods=['DELETE'])
def borrar_miembro(id):
    # This is how you can use the Family datastructure by calling its methods
    try:
        miembro_borrado = jackson_family.delete_member(id)
        response_body = {
                     "family": miembro_borrado}
        return jsonify(response_body), 200
    
    except Exception:
        response_body = {
            "error" : "Error al eliminar a un miembro de la familia"
        }
        return jsonify(response_body), 500

@app.route('/members/<int:id>', methods=['GET'])
def miembro(id):
    # This is how you can use the Family datastructure by calling its methods
    try:
        miembro = jackson_family.get_member(id)
        response_body = {
                     "family": miembro}
        return jsonify(response_body), 200
    except Exception:
        response_body = {
            "error" : "Error al recuperar a un miembro de la familia"
        }
        return jsonify(response_body), 500

@app.route('/members/<int:id>', methods=['PUT'])
def actualizar_miembro(id):
    try:
        actualizacion_miembro = request.json
        miembro_actualizado = jackson_family.update_member(id, actualizacion_miembro)
        response_body = {
                     "family": miembro_actualizado}
        return jsonify(response_body), 200
    except Exception:
        response_body = {
            "error" : "Error al actualizar a un miembro de la familia"
        }
        return jsonify(response_body), 500



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
