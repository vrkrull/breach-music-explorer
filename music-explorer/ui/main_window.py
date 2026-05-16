from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from functools import partial

from core.search_engine import SearchEngine
from api.cover import cover
from api.deezer import get_preview
from utils.cache import load


class MusicApp(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Spotify Mode Music Explorer")
        self.setMinimumSize(1500, 900)

        # AUDIO
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)

        # RIGHT PANEL
        self.cover = QLabel()
        self.cover.setFixedSize(350, 350)

        self.info = QLabel()
        self.info.setWordWrap(True)

        self.tracklist = QListWidget()

        right = QVBoxLayout()
        right.addWidget(self.cover)
        right.addWidget(self.info)
        right.addWidget(QLabel("Tracks"))
        right.addWidget(self.tracklist)

        # RESULTS
        self.results = QWidget()
        self.layout = QVBoxLayout(self.results)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.results)

        # SEARCH
        self.q = QLineEdit()
        self.q.setPlaceholderText("Search anything (Chrono Trigger, FF7, Mitsuda...)")

        btn = QPushButton("Search")
        btn.clicked.connect(self.search)

        top = QHBoxLayout()
        top.addWidget(self.q)
        top.addWidget(btn)

        main = QHBoxLayout()
        main.addWidget(scroll, 3)
        main.addLayout(right, 2)

        root = QVBoxLayout()
        root.addLayout(top)
        root.addLayout(main)

        w = QWidget()
        w.setLayout(root)
        self.setCentralWidget(w)

    # ---------------- SEARCH ----------------

    def search(self):

        self.clear()

        q = self.q.text().strip()

        tracks = SearchEngine.tracks(q)
        albums = SearchEngine.albums(q)

        self.label("🎵 Tracks")

        for t in tracks[:25]:

            title = t.get("title")

            btn = QPushButton(title)
            btn.clicked.connect(
                partial(self.open_track, t)
            )

            self.layout.addWidget(btn)

        self.label("💿 Albums")

        for a in albums:

            btn = QPushButton(a.get("title"))
            btn.clicked.connect(
                partial(self.open_album, a)
            )

            self.layout.addWidget(btn)

    # ---------------- TRACK ----------------

    def open_track(self, t):

        title = t.get("title")

        self.info.setText(f"Track: {title}")

        releases = t.get("releases", [])

        if releases:

            img = cover(releases[0]["id"])

            if img:
                pix = load(img)

                if pix:
                    self.cover.setPixmap(
                        pix.scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio)
                    )

        # AUDIO PREVIEW
        preview = get_preview(title)

        if preview:
            self.player.setSource(QUrl(preview))
            self.player.play()

    # ---------------- ALBUM ----------------

    def open_album(self, a):

        self.info.setText(f"Album: {a.get('title')}")

        self.tracklist.clear()

        # fake album expansion (MusicBrainz limitation)
        self.tracklist.addItem("Loading album tracks...")

    # ---------------- UI HELPERS ----------------

    def label(self, text):

        l = QLabel(text)
        l.setStyleSheet("font-size:18px;font-weight:bold;")
        self.layout.addWidget(l)

    def clear(self):

        for i in reversed(range(self.layout.count())):
            w = self.layout.itemAt(i).widget()
            if w:
                w.deleteLater()