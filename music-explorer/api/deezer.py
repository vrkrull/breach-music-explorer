import requests


def get_preview(title, artist=""):

    q = f"{title} {artist}"

    r = requests.get(
        "https://api.deezer.com/search",
        params={"q": q}
    ).json()

    data = r.get("data", [])

    if not data:
        return None

    return data[0].get("preview")