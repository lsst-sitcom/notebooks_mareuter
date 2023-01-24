from .playlist import Playlist

__all__ = ["TTS_PLAYLISTS"]

FILE_STEM = "AT_{0}_{1}_{2:06}"

TTS_PLAYLISTS = {
    "default": Playlist(20210218, list(range(249, 263 + 1)), "O", "emu", FILE_STEM),
    "bias": Playlist(20211007, list(range(43, 52 + 1)), "O", "emu", FILE_STEM),
    "dark": Playlist(20211007, list(range(53, 62 + 1)), "O", "emu", FILE_STEM),
    "flat": Playlist(20211007, list(range(63, 72 + 1)), "O", "emu", FILE_STEM),
    "ptc": Playlist(20211007, list(range(73, 112 + 1)), "O", "emu", FILE_STEM),
    "cwfs": Playlist(
        20211104, [950, 951, 954, 955, 958, 959, 960], "O", "emu", FILE_STEM
    ),
    "standard_visit": Playlist(
        20210121, list(range(739, 743 + 1)), "O", "emu", FILE_STEM
    ),
    "pointing": Playlist(20200314, list(range(188, 192 + 1)), "O", "emu", FILE_STEM),
    "verify": Playlist(20210217, list(range(325, 329 + 1)), "O", "emu", FILE_STEM),
    "test": Playlist(20200315, list(range(120, 122 + 1)), "O", "emu", FILE_STEM),
}
