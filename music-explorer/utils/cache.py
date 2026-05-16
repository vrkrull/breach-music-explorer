from PyQt6.QtGui import QPixmap
import requests

_cache = {}


def load(url):

    if url in _cache:
        return _cache[url]

    try:
        data = requests.get(url).content
        pix = QPixmap()
        pix.loadFromData(data)

        _cache[url] = pix
        return pix

    except:
        return None