from dataclasses import dataclass

__all__ = ["Playlist"]


@dataclass
class Playlist:
    cam_code: str
    day_obs: int
    seq_nums: list
    controller: str
    daq_folder: str

    def get_image_names(self) -> list:
        file_stem = "{0}_{1}_{2}_{3:06}"
        image_files = []
        for seq_num in self.seq_nums:
            image_files.append(
                file_stem.format(self.cam_code, self.controller, self.day_obs, seq_num)
            )

        return image_files

    def get_image_names_as_string(self, delimiter: str = ":") -> str:
        return delimiter.join(self.get_image_names())
