from flask import Blueprint,request
from .service import Latest,Schedule,Series,ListAll,Detail,Episode,TopAnime
from .result import Result

bp = Blueprint("api", __name__)

@bp.after_request
def add_header(response):
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,PUT,POST,DELETE,OPTIONS"
    return response
    
@bp.route("/latest/")
def latest():
    page = request.args.get("page", 1, type=int)
    try:
        data = Latest(f"https://animekompi.vip/page/{page}")
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/schedule/")
def schedule():
    try:
        data = Schedule("https://animekompi.vip/jadwal-rilis/")
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/populer/")
def populer():
    status = request.args.get("status", "")
    genre = request.args.get("genre", "")
    page = request.args.get("page", 1, type=int)
    try:
        data = Series(f"https://animekompi.vip/anime/?page={page}&status={status}&genre={genre}&order=popular")
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/batch/")
def batch():
    order = request.args.get("order", "")
    genre = request.args.get("genre", "")
    page = request.args.get("page", 1, type=int)
    try:
        data = Series(f"https://animekompi.vip/anime/?page={page}&status=completed&type=tv&genre={genre}&order={order}")
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/series/<type>/")
def movie(type):
    status = request.args.get("status", "")
    order = request.args.get("order", "")
    genre = request.args.get("genre", "")
    page = request.args.get("page", 1, type=int)
    try:
        data = Series(f"https://animekompi.vip/anime/?page={page}&status={status}&type={type}&genre={genre}&order={order}")
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/season/<season>/")
def season(season):
    page = request.args.get("page", 1, type=int)
    try:
        data = Series(f"https://animekompi.vip/anime/?page={page}&season={season}")
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/studio/<studio>/")
def studio(studio):
    page = request.args.get("page", 1, type=int)
    try:
        data = Series(f"https://animekompi.vip/anime/?page={page}&studio={studio}")
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/genre/<genre>/")
def genre(genre):
    page = request.args.get("page", 1, type=int)
    try:
        data = Series(f"https://animekompi.vip/anime/?page={page}&genre={genre}")
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/genres/")
def genres():
    try:
        data = ListAll("https://animekompi.vip/anime/?type=movie&sub=&order=popular", 0)
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/seasons/")
def seasons():
    try:
        data = ListAll("https://animekompi.vip/anime/?type=movie&sub=&order=popular", 1)
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/studios/")
def studios():
    try:
        data = ListAll("https://animekompi.vip/anime/?type=movie&sub=&order=popular", 2)
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/search/")
def search():
    query = request.args.get("query", "")
    page = request.args.get("page", 1, type=int)
    try:
        data = Series(f"https://animekompi.vip/page/{page}/?s={query}")
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/anime/<slug>/")
def detail(slug):
    try:
        data = Detail(f"https://animekompi.vip/anime/{slug}")
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/episode/<slug>/")
def episode(slug):
    try:
        data = Episode(f"https://animekompi.vip/{slug}")
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/top-<date>")
def topanime(date):
    try:
        data = TopAnime("https://animekompi.vip/", date)
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
