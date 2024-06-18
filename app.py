from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User, People, Planet, Favorite 


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///starwarsapi.db"

db.init_app(app)
migrate = Migrate(app, db)


CORS(app, resources={r"/*": {"origins": "*"}})


# Definir rutas
@app.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API SW"})

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hola, Esta es la solicitud GET /user response "
    }
    return jsonify(response_body), 200

# Endpoints para People
@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"msg": "Person no encontrada"}), 404
    return jsonify(person.serialize()), 200

@app.route('/people', methods=['POST'])
def create_person():
    data = request.get_json()
    new_person = People(
        name=data['name'],
        birth_year=data.get('birth_year'),
        gender=data.get('gender'),
        height=data.get('height'),
        skin_color=data.get('skin_color'),
        eye_color=data.get('eye_color')
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 201

# Endpoints para Planets
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    new_planet = Planet(
        name=data['name'],
        climate=data.get('climate'),
        diameter=data.get('diameter'),
        population=data.get('population')
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

# Endpoints para Users
# Dejando un create_user de ejemplo
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not 'email' in data or not 'password' in data:
        return jsonify({"msg": "Bad request, 'email' and 'password' are required"}), 400
    
    new_user = User(
        email=data['email'],
        password=data['password'],  
        is_active=True  
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1  # Placeholder para el ID del usuario actual
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

# Endpoints para Favoritos
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  # Placeholder para el ID del usuario actual
    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 1  # Placeholder para el ID del usuario actual
    favorite = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1  # Placeholder para el ID del usuario actual
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorito eliminado"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = 1  # Placeholder para el ID del usuario actual
    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite is None:
        return jsonify({"msg": "Favorite no encontrado"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorito eliminado"}), 200

# Poblar la base de datos con datos iniciales
def populate_db():
    if People.query.count() == 0:
        people_data = [
            {"name": "Luke Skywalker", "birth_year": "19BBY", "gender": "male", "height": "172", "skin_color": "fair", "eye_color": "blue"},
            {"name": "Darth Vader", "birth_year": "41.9BBY", "gender": "male", "height": "202", "skin_color": "white", "eye_color": "yellow"},
        ]
        for person in people_data:
            new_person = People(**person)
            db.session.add(new_person)

    if Planet.query.count() == 0:
        planet_data = [
            {"name": "Tatooine", "climate": "arid", "diameter": "10465", "population": "200000"},
            {"name": "Alderaan", "climate": "temperate", "diameter": "12500", "population": "2000000000"},
        ]
        for planet in planet_data:
            new_planet = Planet(**planet)
            db.session.add(new_planet)

    if User.query.count() == 0:
        user_data = [
            {"email": "user1@example.com", "password": "password1", "is_active": True},
            {"email": "user2@example.com", "password": "password2", "is_active": True},
        ]
        
        for user in user_data:
            new_user = User(**user)
            db.session.add(new_user)

    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
         db.create_all()
         populate_db()
    app.run(host='localhost', port=5500, debug=True)

