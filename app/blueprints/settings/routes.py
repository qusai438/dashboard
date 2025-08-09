from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import json
import os

settings_bp = Blueprint("settings", __name__, template_folder="../../templates")

SETTINGS_FILE = "settings.json"


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)


@settings_bp.route("/", methods=["GET"])
def settings_home():
    settings = load_settings()
    return render_template("settings.html", settings=settings)


@settings_bp.route("/", methods=["POST"])
def update_settings():
    data = request.form.to_dict()
    save_settings(data)
    flash("Settings updated successfully!", "success")
    return redirect(url_for("settings.settings_home"))


@settings_bp.route("/api", methods=["GET"])
def get_settings_api():
    return jsonify(load_settings())


@settings_bp.route("/api", methods=["POST"])
def update_settings_api():
    data = request.json
    save_settings(data)
    return jsonify({"message": "Settings updated successfully"})
