from datetime import datetime
import os
import pathlib

from astropy.time import Time
from lsst_efd_client import EfdClient
import numpy as np
import pandas as pd
import tables as tb

__all__ = ["DataHandler", "DATETIME_FORMAT", "REPORT_TIME_FORMAT"]


DATETIME_FORMAT = "%Y%m%d_%H%M%S"
REPORT_TIME_FORMAT = "%F %T"
MARKDOWN_SEPARATOR = f"  {os.linesep}"


class DataHandler:
    def __init__(self, data_path: str, date_str: str, pixel_scale: float) -> None:
        self.data_path = pathlib.Path(data_path).expanduser()
        self.centroid_filename = self.data_path / f"smm_centroid_{date_str}.h5"
        self.psd_filename = self.data_path / f"smm_psd_{date_str}.h5"
        self.date_string = date_str
        self.pixel_scale = pixel_scale
        self.general_info: tb.table.Table = None
        self.camera_info: tb.table.Table = None
        self.num_groups: int | None = None
        self.duration: np.timedelta64 = None
        self.psd_x: np.array | None = None
        self.psd_y: np.array | None = None
        self.timestamps: np.array = None
        self.frequencies: np.array | None = None
        self.pd_seeing: pd.DataFrame | None = None
        self.pd_weather: pd.DataFrame | None = None

    async def process(
        self,
        efd_name: str | None = None,
        csc_index: int = 1,
        use_old_weather: bool = False,
    ) -> None:
        self.efd_name = efd_name
        self.use_old_weather = use_old_weather
        self.csc_index = csc_index
        self.__process_psd()
        self.__process_data_info()
        if self.efd_name is None:
            self.__process_data_from_file()
        else:
            await self.__process_data_from_efd()

    def __process_psd(self) -> None:
        psd_h5 = tb.open_file(self.psd_filename)
        glist = psd_h5.root._f_list_nodes(classname="Group")
        keys = [k._v_name for k in glist]
        x_data = []
        y_data = []
        datetimes = []
        # print(keys)
        for i, key in enumerate(keys):
            pd_h5 = pd.read_hdf(self.psd_filename, key=key)
            x_data.append(pd_h5.X.values)
            y_data.append(pd_h5.Y.values)
            datetimes.append(datetime.strptime(key.replace("DT_", ""), DATETIME_FORMAT))
            if i == 0:
                self.frequencies = pd_h5.Frequencies.values
        self.psd_x = np.stack(x_data)
        self.psd_y = np.stack(y_data)
        self.timestamps = np.array(datetimes, dtype=np.datetime64)

    def __process_data_info(self) -> None:
        centroid_h5 = tb.open_file(self.centroid_filename)
        try:
            self.camera_info = centroid_h5.root.camera.info
            self.general_info = centroid_h5.root.general.info
        except tb.NoSuchNodeError:
            pass
        self.num_groups = len(list(centroid_h5.walk_nodes("/", "Array"))) // 4
        self.duration = self.timestamps[-1] - self.timestamps[0]

    def __process_data_from_file(self) -> None:
        centroid_h5 = tb.open_file(self.centroid_filename)
        glist = centroid_h5.root._f_list_nodes(classname="Group")
        keys = [k._v_name for k in glist]
        cx_data = []
        cy_data = []
        sx_data = []
        sy_data = []
        for i, key in enumerate(keys):
            if not key.startswith("DT_"):
                continue
            pd_h5 = pd.read_hdf(self.centroid_filename, key=key)
            x = pd_h5.X.values
            y = pd_h5.Y.values
            cx_data.append(np.mean(x))
            cy_data.append(np.mean(y))
            sx_data.append(self.pixel_scale * np.std(x))
            sy_data.append(self.pixel_scale * np.std(y))
        zero_array = np.zeros(len(cx_data))

        data = {
            "centroidX": cx_data,
            "centroidY": cy_data,
            "rmsX": sx_data,
            "rmsY": sy_data,
            "flux": zero_array,
            "maxADC": zero_array,
            "fwhm": zero_array,
        }
        self.pd_seeing = pd.DataFrame(data=data, index=self.timestamps)
        self.pd_weather = pd.DataFrame(
            data={"speed": zero_array}, index=self.timestamps
        )

    async def __process_data_from_efd(self) -> None:
        client = EfdClient(self.efd_name)
        start = Time(self.timestamps[0])
        end = Time(self.timestamps[-1])
        if self.use_old_weather:
            weather_query = "lsst.sal.Environment.windSpeed"
            weather_index = None
        else:
            weather_query = "lsst.sal.ESS.airFlow"
            weather_index = 301

        self.pd_seeing = await client.select_time_series(
            "lsst.sal.DSM.domeSeeing", "*", start.tai, end.tai, self.csc_index
        )
        self.pd_weather = await client.select_time_series(
            weather_query, "*", start.tai, end.tai, weather_index
        )

    def report_time(self) -> str:
        return datetime.strptime(self.date_string, DATETIME_FORMAT).strftime(
            REPORT_TIME_FORMAT
        )

    def general_information(self) -> str:
        lines = []
        try:
            for name, value in zip(self.general_info.colnames, self.general_info[0]):
                lines.append(f"{name}: {value.decode()}")
        except AttributeError:
            lines.append("No information available!")
        return MARKDOWN_SEPARATOR.join(lines)

    def camera_information(self) -> str:
        lines = []
        try:
            for name, value in zip(self.camera_info.colnames, self.camera_info[0]):
                try:
                    v = value.decode()
                except AttributeError:
                    v = value
                lines.append(f"{name}: {v}")
        except AttributeError:
            lines.append("No information available!")
        return MARKDOWN_SEPARATOR.join(lines)

    def extra_information(self) -> str:
        lines = []
        lines.append(f"Number of data groups: {self.num_groups}")
        lines.append(f"Data Duration (H:M:S): {self.duration.item()}")
        return MARKDOWN_SEPARATOR.join(lines)
