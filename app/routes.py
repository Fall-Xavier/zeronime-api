import cloudscraper,random,re
from bs4 import BeautifulSoup as parser
from flask import Blueprint,request,jsonify

session = cloudscraper.create_scraper()
bp = Blueprint("api", __name__)

@bp.after_request
def add_header(response):
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,PUT,POST,DELETE,OPTIONS"
    return response

def add_requests(params):
    response = parser(session.get("https://bacakomik.one/"+params).text, "html.parser")
    return response
    
def remove_nondigit(text):
    return re.sub(r"\D","", text)
    
@bp.route("/latest/page/<page>")
def scrape_latest(page):
    try:
        response = add_requests("komik-terbaru")
        komik_list = []
        for element in response.select(".animepost"):
            title = element.select_one("h4").get_text(strip=True)
            link = element.select_one("a")["href"]
            cover = element.select_one("img")["data-lazy-src"]
            chapter = remove_nondigit(element.select_one(".lsch a").get_text(strip=True))
            date = element.select_one(".datech").get_text(strip=True)
            type_tag = element.select_one("span.typeflag.Manhwa") or element.select_one("span.typeflag.Manhua")
            type = "manhwa" if "Manhwa" in str(type_tag) else "manhua" if "Manhua" in str(type_tag) else "manga"
            komik_list.append({"title": title, "link": link, "cover": cover, "chapter": chapter, "date": date, "type": type})
        next_page = bool(response.select_one("a.next.page-numbers"))
        return jsonify({"komikList": komik_list, "nextPage": next_page})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/search/<query>/page/<page>")
def scrape_search(query,page):
    try:
        response = add_requests(f"page/{page}/?s={query}")
        komik_list = []
        for element in response.select(".animepost"):
            title = element.select_one("h4").get_text(strip=True)
            link = element.select_one("a")["href"]
            cover = element.select_one("img")["src"]
            rating = element.select_one(".rating i").get_text(strip=True)
            type_tag = element.select_one("span.typeflag.Manhwa") or element.select_one("span.typeflag.Manhua")
            type = "manhwa" if "Manhwa" in str(type_tag) else "manhua" if "Manhua" in str(type_tag) else "manga"
            komik_list.append({"title": title, "link": link, "cover": cover, "rating": rating, "type": type})
        next_page = bool(response.select_one("a.next.page-numbers"))
        return jsonify({"komikList": komik_list, "nextPage": next_page})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@bp.route("/populer/page/<page>")
def scrape_populer(page):
    try:
        response = add_requests(f"komik-populer/page/{page}")
        komik_list = []
        for element in response.select(".animepost"):
            title = element.select_one("h4").get_text(strip=True)
            link = element.select_one("a")["href"]
            cover = element.select_one("img")["data-lazy-src"]
            rating = element.select_one(".rating i").get_text(strip=True)
            type_tag = element.select_one("span.typeflag.Manhwa") or element.select_one("span.typeflag.Manhua")
            type = "manhwa" if "Manhwa" in str(type_tag) else "manhua" if "Manhua" in str(type_tag) else "manga"
            komik_list.append({"title": title, "link": link, "cover": cover, "rating": rating, "type": type})
        next_page = bool(response.select_one("a.next.page-numbers"))
        return jsonify({"komikList": komik_list, "nextPage": next_page})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@bp.route("/only-<type>/page/<page>")
def scrape_onlytype(type,page):
    try:
        response = add_requests(f"baca-{type}/page/{page}")
        komik_list = []
        for element in response.select(".animepost"):
            title = element.select_one("h4").get_text(strip=True)
            link = element.select_one("a")["href"]
            cover = element.select_one("img")["data-lazy-src"]
            chapter = remove_nondigit(element.select_one(".lsch a").get_text(strip=True))
            date = element.select_one(".datech").get_text(strip=True)
            type_tag = element.select_one("span.typeflag.Manhwa") or element.select_one("span.typeflag.Manhua")
            type = "manhwa" if "Manhwa" in str(type_tag) else "manhua" if "Manhua" in str(type_tag) else "manga"
            komik_list.append({"title": title, "link": link, "cover": cover, "chapter": chapter, "date": date, "type": type})
        next_page = bool(response.select_one("a.next.page-numbers"))
        return jsonify({"komikList": komik_list, "nextPage": next_page})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@bp.route("/recomen")
def scrape_recomen():
    try:
        response = add_requests(f"genres/action")
        komik_list = []
        for element in response.select(".serieslist li"):
            try:
                title = element.select_one("h4").get_text(strip=True)
                link = element.select_one("a.series")["href"]
                cover = element.select_one("img")["data-lazy-src"]
                rating = element.select_one("span.loveviews").get_text(strip=True)
                genre = element.select_one("span.genre").get_text(strip=True)
                komik_list.append({"title": title, "link": link, "cover": cover, "rating": rating, "genre": genre})
            except:pass
        return jsonify(komik_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@bp.route("/top")
def scrape_top():
    try:
        response = add_requests(f"komik-populer")
        komik_list = []
        for element in response.select(".serieslist.pop li"):
            title = element.select_one("h4").get_text(strip=True)
            link = element.select_one("a")["href"]
            cover = element.select_one("img")["data-lazy-src"]
            rating = element.select_one("span.loveviews").get_text(strip=True)
            komik_list.append({"title": title, "link": link, "cover": cover, "rating": rating})
        return jsonify(komik_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@bp.route("/all-list")
def scrape_all_list():
    try:
        response = add_requests(f"daftar-komik/?list")
        
        author = []
        for element in response.select(".dropdown-menu.c4")[0].find_all("li"):
            title = element.get_text(strip=True)
            link = element.find("input")["value"]
            author.append({"title": title, "link": link})
        
        artist = []
        for element in response.select(".dropdown-menu.c4")[1].find_all("li"):
            title = element.get_text(strip=True)
            link = element.find("input")["value"]
            artist.append({"title": title, "link": link})
        
        genres = []
        for element in response.select(".dropdown-menu.c4")[2].find_all("li"):
            title = element.get_text(strip=True)
            link = element.find("input")["value"]
            genres.append({"title": title, "link": link})
        
        release = []
        for element in response.select(".dropdown-menu.c4")[3].find_all("li"):
            title = element.get_text(strip=True)
            link = element.find("input")["value"]
            release.append({"title": title, "link": link})
        
        status = []
        for element in response.select(".dropdown-menu.c1")[0].find_all("li"):
            title = element.get_text(strip=True)
            link = element.find("input")["value"]
            status.append({"title": title, "link": link})
        
        type = []
        for element in response.select(".dropdown-menu.c1")[1].find_all("li"):
            title = element.get_text(strip=True)
            link = element.find("input")["value"]
            type.append({"title": title, "link": link})
        
        orderby = []
        for element in response.select(".dropdown-menu.c1")[2].find_all("li"):
            title = element.get_text(strip=True)
            link = element.find("input")["value"]
            orderby.append({"title": title, "link": link})
        
        return jsonify({"author": author, "artist": artist, "genres": genres, "release": release, "status": status, "type": type, "orderby": orderby})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@bp.route("/komik/<komik>")
def scrape_detail(komik):
    try:
        response = add_requests(f"komik/{komik}")
        title = response.select_one(".postbody h1").get_text(strip=True).replace("Komik", "").strip()
        cover = response.select_one(".postbody img")["data-lazy-src"]
        first_chapter = {
            "title": response.select(".postbody .epsbr")[0].select_one("span.barunew").get_text(strip=True).replace("Chapter", "").replace(" ", ""),
            "link": response.select(".postbody .epsbr")[0].select_one("a")["href"]
        }
        last_chapter = {
            "title": response.select(".postbody .epsbr")[1].select_one("span.barunew").get_text(strip=True).replace("Chapter", "").replace(" ", ""),
            "link": response.select(".postbody .epsbr")[1].select_one("a")["href"]
        }
        rating = response.select_one(".postbody .rtg").get_text(strip=True).replace(" ", "") if response.select_one(".postbody .rtg") else "0"
        infox = response.select(".infox .spe span")
        other_title = infox[0].get_text(strip=True).split(":")[1].strip() if len(infox) > 0 else ""
        status = infox[1].get_text(strip=True).split(":")[1].strip() if len(infox) > 1 else ""
        type = infox[2].get_text(strip=True).split(":")[1].strip() if len(infox) > 2 else ""
        author = infox[3].get_text(strip=True).split(":")[1].strip() if len(infox) > 3 else ""
        artist = infox[4].get_text(strip=True).split(":")[1].strip() if len(infox) > 4 else ""
        release = infox[5].get_text(strip=True).split(":")[1].strip() if len(infox) > 5 else ""
        series = infox[6].get_text(strip=True).split(":")[1].strip() if len(infox) > 6 else ""
        reader = infox[7].get_text(strip=True).split(":")[1].strip() if len(infox) > 7 else ""

        synopsis = response.select_one(".postbody [itemprop='description']").get_text().replace("\n","").strip()

        genres = [
            {"title": genre.get_text(strip=True), "link": genre["href"]}
            for genre in response.select(".postbody .genre-info a")
        ]
        chapters = [
            {
                "title": remove_nondigit(chapter.select_one("span.lchx a")["href"] if chapter.select_one("span.lchx a") else ""),
                "link": chapter.select_one("span.lchx a")["href"] if chapter.select_one("span.lchx a") else "",
                "date": chapter.select_one("span.dt").get_text(strip=True) if chapter.select_one("span.dt") else ""
            }
            for chapter in response.select(".postbody #chapter_list li")
        ]

        return jsonify({"title": title, "cover": cover, "firstChapter": first_chapter, "lastChapter": last_chapter, "rating": rating, "otherTitle": other_title, "status": status, "type": type, "author": author, "artist": artist, "release": release, "reader": reader, "synopsis": synopsis, "genres": genres, "chapters": chapters})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
        
@bp.route("/chapter/<chapter>")
def scrape_chapter(chapter):
    try:
        response = add_requests(f"{chapter}")
        title = response.select_one(".dtlx h1").get_text().replace("Komik", "").strip()
        images = [
            img["data-lazy-src"]
            for img in response.select("#anjay_ini_id_kh img")
            if img.get("data-lazy-src")
        ]
        next_page = bool(response.select(".nextprev a[rel='next']"))
        return jsonify({"title": title, "images": images, "nextPage": next_page})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        