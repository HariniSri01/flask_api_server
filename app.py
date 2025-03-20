from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_database"
mongo = PyMongo(app)

# 🟢 READ: Get all users
@app.route("/users", methods=["GET"])
def get_users():
    users = list(mongo.db.users.find({}, {"_id": 0}))  # Exclude the ObjectId
    return jsonify(users)

# 🟢 READ: Get a user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = mongo.db.users.find_one({"id": user_id}, {"_id": 0})
    return jsonify(user) if user else ("User not found", 404)

# 🔵 CREATE: Add a new user
@app.route("/users", methods=["POST"])
def add_user():
    new_user = request.json
    mongo.db.users.insert_one(new_user)
    return jsonify(new_user), 201

# 🟡 UPDATE: Modify an existing user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    updated_data = request.json
    result = mongo.db.users.update_one({"id": user_id}, {"$set": updated_data})
    if result.matched_count == 0:
        return ("User not found", 404)
    return jsonify({"message": "User updated successfully"})

# 🔴 DELETE: Remove a user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = mongo.db.users.delete_one({"id": user_id})
    if result.deleted_count == 0:
        return ("User not found", 404)
    return jsonify({"message": "User deleted successfully"})

@app.route("/")
def home():
    return "Welcome to the MongoDB-powered Flask API!"

if __name__ == "__main__":
    app.run(debug=True)
