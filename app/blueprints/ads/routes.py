from flask import Blueprint, request, jsonify
from app.services.ad_service import AdService

ads_bp = Blueprint("ads", __name__)
ad_service = AdService()


@ads_bp.route("/generate", methods=["POST"])
def generate_ad():
    data = request.json
    product_images = data.get("images", [])
    platform = data.get("platform", "all")
    campaign_type = data.get("campaign_type", "default")

    if not product_images:
        return jsonify({"error": "No product images provided"}), 400

    try:
        ad_content = ad_service.generate_campaign(product_images, platform, campaign_type)
        return jsonify({"ad_content": ad_content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ads_bp.route("/publish", methods=["POST"])
def publish_ad():
    data = request.json
    platform = data.get("platform")
    ad_content = data.get("ad_content")

    if not platform or not ad_content:
        return jsonify({"error": "Platform and ad content are required"}), 400

    try:
        result = ad_service.publish(platform, ad_content)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
