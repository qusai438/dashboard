from flask import Blueprint, current_app, jsonify, request
import os
import json
from pathlib import Path
from typing import Any, Dict

settings_bp = Blueprint("settings", __name__)

SETTINGS_FILE = "settings.json"


def _instance_path() -> Path:
    base = Path(current_app.instance_path)
    base.mkdir(parents=True, exist_ok=True)
    return base


def _settings_path() -> Path:
    return _instance_path() / SETTINGS_FILE


def _load_settings() -> Dict[str, Any]:
    p = _settings_path()
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_settings(data: Dict[str, Any]) -> None:
    p = _settings_path()
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


@settings_bp.route("/health", methods=["GET"])
def health() -> Any:
    return jsonify({"status": "ok"}), 200


@settings_bp.route("/", methods=["GET"])
def get_settings() -> Any:
    cfg = current_app.config
    data = _load_settings()
    safe = {
        "FLASK_ENV": cfg.get("FLASK_ENV"),
        "CACHE_TYPE": cfg.get("CACHE_TYPE"),
        "MOCK_MODE": cfg.get("MOCK_MODE", True),
        "REDIS_URL": cfg.get("REDIS_URL") or cfg.get("CELERY_BROKER_URL"),
    }
    return jsonify({"settings": {**safe, **data}}), 200


@settings_bp.route("/", methods=["POST"])
def update_settings() -> Any:
    payload = request.get_json(silent=True) or {}
    allowed = {"MOCK_MODE", "CACHE_TYPE"}
    data = {k: v for k, v in payload.items() if k in allowed}
    if not data:
        return jsonify({"error": "no valid keys"}), 400

    stored = _load_settings()
    stored.update(data)
    _save_settings(stored)

    for k, v in data.items():
        current_app.config[k] = v

    return jsonify({"updated": data}), 200


@settings_bp.route("/mock-mode", methods=["POST"])
def toggle_mock_mode() -> Any:
    payload = request.get_json(silent=True) or {}
    value = payload.get("enabled")
    if isinstance(value, bool):
        current_app.config["MOCK_MODE"] = value
        stored = _load_settings()
        stored["MOCK_MODE"] = value
        _save_settings(stored)
        return jsonify({"MOCK_MODE": value}), 200
    return jsonify({"error": "invalid value"}), 400
