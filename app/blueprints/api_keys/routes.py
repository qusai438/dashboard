from flask import Blueprint, request, jsonify, current_app
from cryptography.fernet import Fernet
import os
import json

api_keys_bp = Blueprint("api_keys", __name__)

KEYS_FILE = "api_keys.json"
ENCRYPTION_KEY_FILE = "encryption.key"


def get_encryption_key():
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(ENCRYPTION_KEY_FILE, "rb") as f:
            key = f.read()
    return Fernet(key)


def load_keys():
    if not os.path.exists(KEYS_FILE):
        return {}
    with open(KEYS_FILE, "r") as f:
        return json.load(f)


def save_keys(keys):
    with open(KEYS_FILE, "w") as f:
        json.dump(keys, f)


@api_keys_bp.route("/", methods=["GET"])
def list_keys():
    fernet = get_encryption_key()
    keys = load_keys()
    decrypted = {k: fernet.decrypt(v.encode()).decode() for k, v in keys.items()}
    return jsonify(decrypted)


@api_keys_bp.route("/", methods=["POST"])
def add_key():
    data = request.json
    if "name" not in data or "value" not in data:
        return jsonify({"error": "Missing name or value"}), 400

    fernet = get_encryption_key()
    keys = load_keys()
    keys[data["name"]] = fernet.encrypt(data["value"].encode()).decode()
    save_keys(keys)
    return jsonify({"message": "Key saved successfully"})


@api_keys_bp.route("/<name>", methods=["DELETE"])
def delete_key(name):
    keys = load_keys()
    if name not in keys:
        return jsonify({"error": "Key not found"}), 404
    del keys[name]
    save_keys(keys)
    return jsonify({"message": "Key deleted successfully"})
