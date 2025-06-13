"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Characters,Planets,Vehicles,Fav_planet,Fav_character
from flask import request
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GETS
# all users
@app.route('/user', methods=['GET'])
def get_users():
  try:
      query_results= User.query.all()
      results=[item.serialize() for item in query_results]
    #   results= list(map(lambda item: item.serialize(), query_results))
    #   if not query_results:
    #        return jsonify({"msg": "Usuario no encontrado"}), 400

      response_body = {
        "msg": "Everything its ok",
        "result": results
    }

      return jsonify(response_body), 200
  
  except Exception as e: 
      print(f"Error al obtener usuarios: {e}")
      return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
  
  

# user by id
@app.route('/user/<int:user_id>', methods=['GET'])
def user_by_id(user_id):
  try:
       query_user= User.query.filter_by(id=user_id).first()
       
       if not query_user:
           return jsonify({"msg": "Usuario no encontrado"}), 404
       
       response_body = {
           "msg": "Everything its ok",
           "result": query_user.serialize()
       }
   
       return jsonify(response_body), 200
  
  except Exception as e: 
      print(f"Error al obtener usuario: {e}")
      return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
  


# All Characters
@app.route('/characters>', methods=['GET'])
def get_characters():
  try:

       query_results= Characters.query.all()
       if not query_results:
           return jsonify({"msg": "Personaje no encontrado"}), 400
       
       results= list(map(lambda item: item.serialize(), query_results))
 
       response_body = {
         "msg": "Everything its ok",
         "result": results
        }

       return jsonify(response_body), 200
    
  except Exception as e: 
      print(f"Error al obtener personaje: {e}")
      return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500



# Characters by id
@app.route('/character/<int:character_id>', methods=['GET'])
def character_by_id(character_id):
   try:
       query_character= Characters.query.filter_by(id=character_id).first()

       if not query_character:
           return jsonify({"msg": "Personaje no encontrado"}), 400
   
       response_body = {
           "msg": "Everything its ok",
           "result": query_character.serialize()
       }
   
       return jsonify(response_body), 200
   except Exception as e: 
      print(f"Error al obtener usuario: {e}")
      return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

# All Planets
@app.route('/planets>', methods=['GET'])
def get_planets():
  try:

       query_results= Planets.query.all()
       if not query_results:
           return jsonify({"msg": "Error en la solicitud"}), 400
       
       results= list(map(lambda item: item.serialize(), query_results))
 
       response_body = {
         "msg": "Everything its ok",
         "result": results
        }

       return jsonify(response_body), 200
    
  except Exception as e: 
      print(f"Error al obtener planetas: {e}")
      return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500



# Planets by id
@app.route('/planet/<int:planet_id>', methods=['GET'])
def planet_by_id(planet_id):
  try:
       query_planet= Planets.query.filter_by(id=planet_id).first()
       
       if not query_planet:
           return jsonify({"msg": "No se encontró planeta"}), 400
       
       response_body = {
           "msg": "Everything its ok",
           "result": query_planet.serialize()
       }
   
       return jsonify(response_body), 200
  
  except Exception as e: 
      print(f"Error al obtener planeta: {e}")
      return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


# All Vehicles
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
  try:

       query_results= Vehicles.query.all()
       if not query_results:
           return jsonify({"msg": "Error en la solicitud"}), 400
       
       results= list(map(lambda item: item.serialize(), query_results))
 
       response_body = {
         "msg": "Everything its ok",
         "result": results
        }

       return jsonify(response_body), 200
    
  except Exception as e: 
      print(f"Error al obtener vehículos: {e}")
      return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
  
  
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def vehicles_by_id(vehicle_id):
   try:
       query_vehicle= Vehicles.query.filter_by(id=vehicle_id).first()

       if not query_vehicle:
           return jsonify({"msg": "Vehículo no encontrado"}), 400
   
       response_body = {
           "msg": "Everything its ok",
           "result": query_vehicle.serialize()
       }
   
       return jsonify(response_body), 200
   except Exception as e: 
      print(f"Error al obtener vehiculo: {e}")
      return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500



#POST
#POST usuario
@app.route('/user', methods=['POST'])
def create_user():
    data=request.get_json()

    if not data:
        return jsonify({"msg": "No se proporcionaron datos"}),400
    name = data.get("name")
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")
    is_active = data.get("is_active", False)

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "Ya existe un usuario con este email"}), 409
    
    new_user = User(
        name=name,
        user_name=user_name,
        email=email,
        password=password,
        is_active=is_active
    )
    db.session.add(new_user)

    try:
        db.session.commit()
        return jsonify(new_user.serialize()),201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f'Internal Server Error, "error": {str(e)}'}), 500
    

@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):

    user= User.query.get(user_id)
    if not user:
        return jsonify({"msg": "El usuario no existe"}), 404
    planet= Planets.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "El planeta no existe"}), 404
    
    favorite_exist= Fav_planet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite_exist:
        return jsonify({"msg": "El favorito ya existe dentro de la tabla"}), 403
    

    new_planet_fav = Fav_planet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_planet_fav)
    db.session.commit()

    return jsonify({"msg": "Favorito agregado correctamente"}), 201


@app.route('/user/<int:user_id>/favorites_characters/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):

    user= User.query.get(user_id)
    if not user:
        return jsonify({"msg": "El usuario no existe"}), 404
    character= Characters.query.get(character_id)
    if not character:
        return jsonify({"msg": f'{character.name} ya está en tu lista de favoritos'}), 404
    
    favorite_exist= Fav_character.query.filter_by(user_id=user_id, character_id=character_id).first()
    if favorite_exist:
        return jsonify({"msg": "El favorito ya existe dentro de la tabla"}), 403
    

    new_character_fav = Fav_character(user_id=user_id, character_id=character_id)
    db.session.add(new_character_fav)
    db.session.commit()

    return jsonify({"msg": f'{character.name} agregado correctamente'}), 201 


#DELETE
#Delete Character

@app.route('/user/<int:user_id>/favorites_characters/<int:character_id>', methods=['DELETE'])
def delete_fav_character(user_id, character_id):
    user = User.query.get(user_id)
    character = Characters.query.get(character_id)

    if not user:
        return jsonify({'msg': 'Usuario no encontrado'}), 404
    if not character:
        return jsonify({'msg': 'Personaje no encontrado'}), 404

    fav_character =Fav_character.query.filter_by(
        user_id=user_id, character_id=character_id).first()
    if not fav_character:
        return jsonify({'msg': f'{character.name} no encontrado en la lista'}), 404

    db.session.delete(fav_character)
    db.session.commit()
    return jsonify({'msg': f'{character.name} a sido eliminado de la lista'})

#Delete Planet
@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if not user:
        return jsonify({'msg': 'Usuario no encontrado'}), 404
    if not planet:
        return jsonify({'msg': 'Planeta no encontrado'}), 404

    fav_planet =Fav_planet.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if not fav_planet:
        return jsonify({'msg': f'{planet.name} no encontrado en la lista'}), 404

    db.session.delete(fav_planet)
    db.session.commit()
    return jsonify({'msg': f'{planet.name} a sido eliminado de la lista'})
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
