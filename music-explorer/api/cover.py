import requests


def cover(release_id):

    try:
        r = requests.get(
            f"https://coverartarchive.org/release/{release_id}"
        )

        if r.status_code != 200:
            return None

        return r.json()["images"][0]["image"]

    except:
        return None