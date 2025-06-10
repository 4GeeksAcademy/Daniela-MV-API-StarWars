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
from models import db, User,Characters,Planets,Vehicles
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
      results= list(map(lambda item: item.serialize(), query_results))
      if not query_results:
           return jsonify({"msg": "Usuario no encontrado"}), 400

      response_body = {
        "msg": "Everything its ok",
        "result": results
    }

      return jsonify(response_body), 200
  
  except Exception as e: 
      print(f"Erro al obtener usuarios: {e}")
      return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
  
  

# user by id
@app.route('/user/<int:user_id', methods=['GET'])
def user_by_id(user_id):
  try:
       query_user= User.query.filter_by(id=user_id).first()
       
       if not query_user:
           return jsonify({"msg": "Usuario no encontrado"}), 400
       
       response_body = {
           "msg": "Everything its ok",
           "result": query_user.serialize
       }
   
       return jsonify(response_body), 200
  
  except Exception as e: 
      print(f"Erro al obtener usuario: {e}")
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
      print(f"Erro al obtener personaje: {e}")
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
           "result": query_character.serialize
       }
   
       return jsonify(response_body), 200
   except Exception as e: 
      print(f"Erro al obtener usuario: {e}")
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
      print(f"Erro al obtener planetas: {e}")
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
           "result": query_planet.serialize
       }
   
       return jsonify(response_body), 200
  
  except Exception as e: 
      print(f"Erro al obtener planeta: {e}")
      return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


#POST
#POST usuario
@app.route('/user', methods=['POST'])
def create_user():
    data=request.get_jason()

    if not data:
        return jsonify({"msg": "No se proporcionaron datos"}),400
    email = data.get("email")
    password = data.get("password")
    is_active = data.get("is_active", False)

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "Ya existe un usuario con este email"}), 409
    
    new_user = User(
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

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
