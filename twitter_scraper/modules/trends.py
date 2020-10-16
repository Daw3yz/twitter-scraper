from requests_html import HTML, HTMLSession

session = HTMLSession()


def get_trends():
    trends = []

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "X-Twitter-Active-User": "yes",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "en-US",
    }

    html = session.get("https://twitter.com/trends", headers=headers)

    
    html = HTML(html=html.text, url="bunk", default_encoding="utf-8")

    try:
        trends = [trend.text for trend in html.find("li.topic")]
    except:
        trends = None
    
    return (trends)