from flask import request, jsonify, send_from_directory, current_app as app
from .models import Customer, db
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
mongo_db = client.customer_management
purchase_history = mongo_db.purchase_history

@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'}), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'email': c.email, 'phone': c.phone} for c in customers]), 200

@app.route('/customers/<int:id>/history', methods=['POST'])
def add_purchase(id):
    data = request.json
    purchase_history.update_one({'customer_id': id}, {'$push': {'purchases': data}}, upsert=True)
    return jsonify({'message': 'Purchase added successfully'}), 201

@app.route('/customers/<int:id>/history', methods=['GET'])
def get_purchase_history(id):
    history = purchase_history.find_one({'customer_id': id})
    if history:
        return jsonify(history['purchases']), 200
    return jsonify([]), 200

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    # Remove o histórico de compras do MongoDB
    purchase_history.delete_one({'customer_id': id})
    return jsonify({'message': 'Customer deleted successfully'}), 200

# Rota para servir o arquivo HTML principal
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# Servir arquivos estáticos (CSS, JS)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)
