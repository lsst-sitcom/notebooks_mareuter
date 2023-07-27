import copy

from .playlist import Playlist

__all__ = ["BTS_PLAYLISTS", "TTS_PLAYLISTS"]

TTS_PLAYLISTS = {
    "default": Playlist("AT", 20210218, list(range(249, 263 + 1)), "O", "emu"),
    "bias": Playlist("AT", 20211007, list(range(43, 52 + 1)), "O", "emu"),
    "dark": Playlist("AT", 20211007, list(range(53, 62 + 1)), "O", "emu"),
    "flat": Playlist("AT", 20211007, list(range(63, 72 + 1)), "O", "emu"),
    "ptc": Playlist("AT", 20211007, list(range(73, 112 + 1)), "O", "emu"),
    "cwfs": Playlist("AT", 20211104, [950, 951, 954, 955, 958, 959, 960], "O", "emu"),
    "standard_visit": Playlist("AT", 20210121, list(range(739, 743 + 1)), "O", "emu"),
    "pointing": Playlist("AT", 20200314, list(range(188, 192 + 1)), "O", "emu"),
    "verify": Playlist("AT", 20210217, list(range(325, 329 + 1)), "O", "emu"),
    "test": Playlist("AT", 20200315, list(range(120, 122 + 1)), "O", "emu"),
}

BTS_PLAYLISTS = copy.deepcopy(TTS_PLAYLISTS)
