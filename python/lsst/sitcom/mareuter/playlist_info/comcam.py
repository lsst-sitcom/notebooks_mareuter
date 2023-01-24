from .playlist import Playlist

__all__ = ["TTS_PLAYLISTS"]

TTS_PLAYLISTS = {
    "default": Playlist("CC", 20200221, [10, 20, 124, 163], "C", "emu"),
    "bias": Playlist("CC", 20211123, list(range(1, 10 + 1)), "O", "emu"),
    "dark": Playlist("CC", 20211123, list(range(11, 20 + 1)), "O", "emu"),
    "flat": Playlist("CC", 20211123, list(range(21, 30 + 1)), "O", "emu"),
    "ptc": Playlist("CC", 20211123, list(range(42, 61 + 1)), "O", "emu"),
    "bias2": Playlist("CC", 20211122, list(range(1, 10 + 1)), "O", "emu"),
    "dark2": Playlist("CC", 20211122, list(range(11, 20 + 1)), "O", "emu"),
    "flat2": Playlist("CC", 20211122, list(range(21, 30 + 1)), "O", "emu"),
    "corruption_ncsa": Playlist("CC", 20210910, list(range(22, 71 + 1)), "O", "emu"),
    "cp_pipetask_fail": Playlist("CC", 20211008, list(range(1, 12 + 1)), "O", "emu"),
    "full_cals": Playlist("CC", 20220125, list(range(23, 72 + 1)), "O", "emu"),
    "tiago": Playlist("CC", 20211231, [6001, 6002], "H", "emu2"),
    "aos": Playlist("CC", 20211231, [6001, 6002, 6011, 6012], "H", "emu2"),
}
