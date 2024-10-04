# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, abort, jsonify
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    return {'message': 'Welcome to the pet directory!'}


@app.route('/pet/<int:id>')
def pet_by_id(id):
    pet = Pet.query.get(id)
    if not pet:
        return {'message': f'Pet with ID {id} not found.'}, 404

    return {'id': pet.id, 'name': pet.name, 'species': pet.species}


@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = Pet.query.filter_by(species=species.capitalize()).all()

    if not pets:
        return {'message': f'No Pets found with species {species}'}, 404

    return {
        'count': len(pets),
        'pets': [{
            'id': pet.id,
            'name': pet.name,
        } for pet in pets]
    }


if __name__ == '__main__':
    app.run(port=5555, debug=True)
