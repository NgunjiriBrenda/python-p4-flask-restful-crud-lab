from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

# ======== EXISTING ROUTES (probably already there) ========
@app.route('/')
def index():
    return 'Plant Store API'

@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants])

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get(id)
    if plant:
        return jsonify(plant.to_dict())
    return jsonify({'error': 'Plant not found'}), 404

# ======== YOUR NEW ROUTES GO HERE ========

# UPDATE ROUTE - PATCH /plants/:id
@app.route('/plants/<int:id>', methods=['PATCH'])  # 👈 This goes here
def update_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    
    data = request.get_json()
    
    # Update only the fields provided
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']
    
    db.session.commit()
    return jsonify(plant.to_dict()), 200

# DELETE ROUTE - DELETE /plants/:id  
@app.route('/plants/<int:id>', methods=['DELETE'])  # 👈 This goes here
def delete_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    
    db.session.delete(plant)
    db.session.commit()
    return '', 204

# ======== END OF ROUTES ========
if __name__ == '__main__':
    app.run(port=5555, debug=True)