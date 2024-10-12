from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
CORS(app)

# Update this to match your actual PostgreSQL connection information
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Product model updated to match the schema in db.init
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Use Numeric for DECIMAL type
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': str(self.price),  # Cast price to string for JSON serialization
            'stock_quantity': self.stock_quantity,
            'created_at': self.created_at
        }

@app.route('/api/db-check', methods=['GET'])
def check_db_connection():
    try:
        # Attempt to query the database
        Product.query.limit(1).all()
        return jsonify({"status": "success", "message": "Connected to the database successfully"}), 200
    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": f"Database connection failed: {str(e)}"}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(
        name=data['name'], 
        description=data.get('description', ''),
        price=data['price'],
        stock_quantity=data.get('stock_quantity', 0)
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
    db.session.commit()
    return jsonify(product.to_dict())

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
