from flask import Blueprint,jsonify

bp = Blueprint("/", __name__)

@bp.route("/")
def index():
    return jsonify({"status":"online", "text":"Server Zeronime Ready For Use"}), 200
