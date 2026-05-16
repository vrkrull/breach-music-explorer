import requests
from rapidfuzz import fuzz
from core.vgm import vgm_score


class SearchEngine:

    @staticmethod
    def tracks(query):

        r = requests.get(
            "https://musicbrainz.org/ws/2/recording/",
            params={"query": query, "fmt": "json", "limit": 50},
            headers={"User-Agent": "SpotifyClone/1.0"}
        ).json()

        recs = r.get("recordings", [])

        def score(x):
            title = x.get("title", "")
            return (
                vgm_score(title, query) +
                fuzz.partial_ratio(query.lower(), title.lower())
            )

        recs.sort(key=score, reverse=True)
        return recs

    @staticmethod
    def albums(query):

        r = requests.get(
            "https://musicbrainz.org/ws/2/release-group/",
            params={"query": query, "fmt": "json", "limit": 30},
            headers={"User-Agent": "SpotifyClone/1.0"}
        ).json()

        return r.get("release-groups", [])