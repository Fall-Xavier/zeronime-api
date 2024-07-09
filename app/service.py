import cloudscraper,base64
from bs4 import BeautifulSoup as parser
session = cloudscraper.create_scraper()

def Latest(url):
    data = {}
    response = session.get(url)
    parsing = parser(response.text, "html.parser")
    soup = parsing.find("div",{"class":"listupd normal"})
    anime = []
    for item in soup.find_all("article"):
        title = item.find("a").get("title").split(" Episode")[0]
        slug = item.find("a").get("href").split("/")[3]
        cover = item.find_all("img")[1].get("src")
        episode = item.find("span",{"class":"epx"}).text.replace("Ep ","")
        type = item.find("div",{"class":"typez"}).text
        anime.append({"title": title, "slug": slug, "cover": cover, "episode": episode, "type": type})
    data.update({"anime":anime})
    try:
        for next in parsing.find("div",{"class":"hpage"}).find_all("a"):
            if "Selanjutnya" in str(next):
                data.update({"next": next.get("href").replace("https://animekompi.vip/","")})
    except:
        data.update({"next": "notfound"})
    return data
     
def Schedule(url):
    data = []
    response = session.get(url)
    parsing = parser(response.text, "html.parser")
    soup = parsing.find("div",{"class":"postbody"})
    for item in soup.find_all("div",{"class":"bixbox"}):
        try:
            day = item.find("div",{"class":"releases"}).text
            if "Jadwal Rilis" in day:
                continue
            animeList = {"day": day, "anime": []}
            for anime in item.find_all("div",{"class":"bs"}):
                title = item.find("a").get("title")
                slug = item.find("a").get("href").split("/")[4]
                cover = item.find_all("img")[1].get("src")
                episode = item.find("span",{"class":"sb Sub"}).text
                date = item.find("span",{"class":"epx cndwn"}).text
                animeList["anime"].append({"title":title, "slug":slug, "cover":cover, "episode":episode, "date":date})
            data.append(animeList)
        except:
            pass
    return data
        
def Series(url):
    data = {}
    response = session.get(url)
    parsing = parser(response.text, "html.parser")
    soup = parsing.find("div",{"class":"postbody"})
    anime = []
    for item in soup.find_all("article"):
        title = item.find("a").get("title")
        slug = item.find("a").get("href").split("/")[4]
        cover = item.find("img").get("src")
        episode = item.find("span",{"class":"epx"}).text
        type = item.find("div",{"class":"typez"}).text
        anime.append({"title": title, "slug": slug, "cover": cover, "episode": episode, "type": type})
    data.update({"anime":anime})
    try:
        if soup.find("div",{"class":"hpage"}):
            for next in parsing.find("div",{"class":"hpage"}).find_all("a"):
                if "Selanjutnya" in str(next):
                    data.update({"next": next.get("href").replace("https://animekompi.vip/","")})
        elif soup.find("div",{"class":"pagination"}):
            for next in parsing.find("div",{"class":"bixbox"}).find("div",{"class":"pagination"}).find_all("a"):
                if "Next" in str(next):
                    data.update({"next": next.get("href").replace("https://animekompi.vip/","")})
        else:
            data.update({"next": "notfound"})
    except:
        data.update({"next": "notfound"})
    return data
    
def ListAll(url,number):
    data = []
    response = session.get(url)
    parsing = parser(response.text, "html.parser")
    soup = parsing.find_all("div",{"class":"filter dropdown"})[number]
    for item in soup.find("ul",{"class":"dropdown-menu c4 scrollz"}).find_all("li"):
        title = item.text.strip()
        slug = item.find("input").get("value")
        data.append({"title":title, "slug":slug})
    return data
    
def Detail(url):
    data = {}
    response = session.get(url)
    parsing = parser(response.text, "html.parser")
    soup = parsing.find("div",{"class":"postbody"})
    title = soup.find("h1",{"class":"entry-title"}).text
    try:
        alternatif = soup.find("span",{"class":"alter"}).text
    except:
        alternatif = "-"
    cover = soup.find_all("img")[1].get("src")
    try:
        rating = soup.find("div",{"class":"rating"}).find("strong").text.split(" ")[1]
    except:
        rating = "-"
    data.update({"title":title, "alternatif":alternatif, "cover":cover, "rating":rating})
    for item in soup.find("div",{"class":"spe"}).find_all("span"):
        name = item.text.split(": ")[0].replace(" ","").lower()
        value = item.text.split(": ")[1]
        data.update({name:value})
    genre = ",".join(genre.text for genre in soup.find("div",{"class":"genxed"}).find_all("a"))
    data.update({"genre":genre})
    episode = []
    for item in soup.find("div",{"class":"eplister"}).find("ul").find_all("li"):
        title = item.find("div",{"class":"epl-title"}).text
        slug = item.find("a").get("href").split("/")[3]
        eps = item.find("div",{"class":"epl-num"}).text
        date = item.find("div",{"class":"epl-date"}).text
        episode.append({"title":title, "slug":slug, "eps":eps, "date":date})
    data.update({"dataEpisode": episode})
    sinopsis = soup.find("div",{"class":"entry-content"}).text.replace("\n","")
    data.update({"sinopsis": sinopsis})
    return data
    
def Episode(url):
    data = {}
    response = session.get(url)
    parsing = parser(response.text, "html.parser")
    soup = parsing.find("div",{"class":"postbody"})
    title = soup.find("h1",{"class":"entry-title"}).text
    cover = soup.find_all("img")[1].get("src")
    date = soup.find("span",{"class":"updated"}).text
    data.update({"title":title, "cover":cover, "date":date})
    for item in soup.find("div",{"class":"mobius"}).find("select").find_all("option"):
        if "data-index" in str(item):
            index = int(item.get("data-index"))
            decode = base64.b64decode(item.get("value")).decode("utf-8")
            html_format = parser(decode, "html.parser")
            if html_format.find("iframe"):
                link = html_format.find("iframe").get("src")
            elif html_format.find("IFRAME"):
                link = html_format.find("IFRAME").get("SRC")
            if "https" not in link:
                link = f"https:{link}"
            data.update({f"server{index}":link})
    return data
    
