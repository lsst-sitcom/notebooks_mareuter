from .playlist import Playlist

__all__ = ["BTS_PLAYLISTS"]

BTS_PLAYLISTS = {
    "default": Playlist("MC", 20230624, [962], "C", "emu"),
    "bias": Playlist("MC", 20241130, list(range(121, 130 + 1)), "C", "calibration"),
    "dark": Playlist("MC", 20241130, [142, 144] * 5, "C", "calibration"),
    "flat": Playlist("MC", 20241130, [311, 312] * 5, "C", "calibration"),
    "aos-lsstcam-playlist-triplet": Playlist(
        "IM", 20280818, [962, 960, 961], "P", "aos"
    ),
}
