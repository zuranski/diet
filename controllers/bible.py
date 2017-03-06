import requests

@auth.requires_login()
def index():
    r = requests.get("http://labs.bible.org/api/?passage=random")
    xml = XML(r.content)
    return dict(r=r.content)
