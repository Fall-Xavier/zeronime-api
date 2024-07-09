from flask import Blueprint
from .result import Result

bp = Blueprint("/", __name__)

@bp.route("/")
def index():
    return Result("success", "Server Zeronime Ready For Use", 200)
