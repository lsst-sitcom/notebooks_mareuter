from .playlist import Playlist

__all__ = ["TTS_PLAYLISTS"]

FILE_STEM = "CC_O_{0}_{1:06}"

TTS_PLAYLISTS = {
    "bias": Playlist(20211123, list(range(1, 10 + 1)), "emu", FILE_STEM),
    "dark": Playlist(20211123, list(range(11, 20 + 1)), "emu", FILE_STEM),
    "flat": Playlist(20211123, list(range(21, 30 + 1)), "emu", FILE_STEM),
    "ptc": Playlist(20211123, list(range(42, 61 + 1)), "comcam-ptc", FILE_STEM),
    "bias2": Playlist(20211122, list(range(1, 10 + 1)), "emu", FILE_STEM),
    "dark2": Playlist(20211122, list(range(11, 20 + 1)), "emu", FILE_STEM),
    "flat2": Playlist(20211122, list(range(21, 30 + 1)), "emu", FILE_STEM),
    "corruption_ncsa": Playlist(20210910, list(range(22, 71 + 1)), "emu", FILE_STEM),
    "cp_pipetask_fail": Playlist(20211008, list(range(1, 12 + 1)), "emu", FILE_STEM),
    "full_cals": Playlist(20220125, list(range(23, 72 + 1)), "emu", FILE_STEM),
}
