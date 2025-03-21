from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId  # Import ObjectId to handle MongoDB IDs

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_database"
mongo = PyMongo(app)

# Helper function to convert ObjectId to string
def json_converter(user):
    user["_id"] = str(user["_id"])
    return user

# 🟢 READ: Get all users
@app.route("/users", methods=["GET"])
def get_users():
    users = [json_converter(user) for user in mongo.db.users.find()]
    return jsonify(users)

# 🟢 READ: Get a user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = mongo.db.users.find_one({"id": user_id})
    return jsonify(json_converter(user)) if user else ("User not found", 404)

# 🔵 CREATE: Add a new user
@app.route("/users", methods=["POST"])
def add_user():
    try:
        new_user = request.json
        mongo.db.users.insert_one(new_user)
        new_user["_id"] = str(new_user["_id"])  # Convert ObjectId to string
        return jsonify(new_user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 🟡 UPDATE: Modify an existing user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        updated_data = request.json
        result = mongo.db.users.update_one({"id": user_id}, {"$set": updated_data})
        if result.matched_count == 0:
            return ("User not found", 404)
        return jsonify({"message": "User updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 🔴 DELETE: Remove a user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        result = mongo.db.users.delete_one({"id": user_id})
        if result.deleted_count == 0:
            return ("User not found", 404)
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/")
def home():
    return "Welcome to the MongoDB-powered Flask API!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


