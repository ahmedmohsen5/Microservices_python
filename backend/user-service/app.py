from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy


app = Flask(__name__)
CORS(app)

# Replace with actual PostgreSQL credentials and connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model based on the 'users' table in the provided db.init schema
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)  # Matching the VARCHAR(100) in schema
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }

# Route to get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Route to get a user by ID
@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# Route to create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# Route to update an existing user
@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify(user.to_dict())

# Route to delete a user by ID
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# Login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
    return jsonify({"message": "Invalid username or password"}), 401

@app.route('/api/check-db-connection', methods=['GET'])
def check_db_connection():
    try:
        # Attempt to query the database
        db.session.query(sqlalchemy.text('1')).from_statement(sqlalchemy.text('SELECT 1')).all()
        return jsonify({"status": "success", "message": "Database connection is working"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Database connection failed: {str(e)}"}), 500



# Check if the API is running
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
