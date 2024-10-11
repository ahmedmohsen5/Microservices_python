# backend/order-service/app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
CORS(app)
database_url = os.environ.get('DATABASE_URL', 'postgresql://user:password@db/ecommerce')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'status': self.status
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price
        }

@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

@app.route('/api/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify(order.to_dict())

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(user_id=data['user_id'], total_amount=data['total_amount'], status='pending')
    db.session.add(new_order)
    db.session.flush()

    for item in data['items']:
        order_item = OrderItem(order_id=new_order.id, product_id=item['product_id'],
                               quantity=item['quantity'], price=item['price'])
        db.session.add(order_item)

    db.session.commit()
    return jsonify(new_order.to_dict()), 201

@app.route('/api/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get_or_404(id)
    data = request.json
    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify(order.to_dict())

@app.route('/api/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return '', 204


def check_db_connection():
    try:
        db.session.execute('SELECT 1')
        print("Successfully connected to the database!")
        return True
    except SQLAlchemyError as e:
        print(f"Error connecting to the database: {str(e)}")
        return False
@app.route('/health', methods=['GET'])
def health_check():
    if check_db_connection():
        return jsonify({"status": "healthy", "database": "connected"}), 200
    else:
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 500
    

if __name__ == '__main__':
    with app.app_context():
        if check_db_connection():
            db.create_all()  # Create tables if they don't exist
        else:
            print("Failed to connect to the database. Exiting.")
            exit(1)
    
    app.run(host='0.0.0.0', port=5001)