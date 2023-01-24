from .playlist import Playlist

__all__ = ["TTS_PLAYLISTS"]

FILE_STEM = "CC_{0}_{1}_{2:06}"

TTS_PLAYLISTS = {
    "bias": Playlist(20211123, list(range(1, 10 + 1)), "O", "emu", FILE_STEM),
    "dark": Playlist(20211123, list(range(11, 20 + 1)), "O", "emu", FILE_STEM),
    "flat": Playlist(20211123, list(range(21, 30 + 1)), "O", "emu", FILE_STEM),
    "ptc": Playlist(20211123, list(range(42, 61 + 1)), "O", "emu", FILE_STEM),
    "bias2": Playlist(20211122, list(range(1, 10 + 1)), "O", "emu", FILE_STEM),
    "dark2": Playlist(20211122, list(range(11, 20 + 1)), "O", "emu", FILE_STEM),
    "flat2": Playlist(20211122, list(range(21, 30 + 1)), "O", "emu", FILE_STEM),
    "corruption_ncsa": Playlist(
        20210910, list(range(22, 71 + 1)), "O", "emu", FILE_STEM
    ),
    "cp_pipetask_fail": Playlist(
        20211008, list(range(1, 12 + 1)), "O", "emu", FILE_STEM
    ),
    "full_cals": Playlist(20220125, list(range(23, 72 + 1)), "O", "emu", FILE_STEM),
    "tiago": Playlist(20211231, [6001, 6002], "H", "emu2", FILE_STEM),
    "aos": Playlist(20211231, [6001, 6002, 6011, 6012], "H", "emu2", FILE_STEM),
}
