from dataclasses import dataclass

__all__ = ["Playlist"]


@dataclass
class Playlist:
    day_obs: int
    seq_nums: list
    daq_folder: str
    file_stem: str

    def get_image_names(self) -> list:
        image_files = []
        for seq_num in self.seq_nums:
            image_files.append(self.file_stem.format(self.day_obs, seq_num))

        return image_files

    def get_image_names_as_string(self) -> str:
        return ":".join(self.get_image_names())
