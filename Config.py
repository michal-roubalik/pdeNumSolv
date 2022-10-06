import pandas as pd


class Config:
    def __init__(self, cfg_file_path) -> None:
        self.cfg_file_path = cfg_file_path
        self.N = 11
        self.equation_type = self.load_cfg_param(
            param_type="EquationType", cfg_file_path=cfg_file_path
        )
        self.solution_scheme = self.load_cfg_param(
            param_type="SolutionScheme", cfg_file_path=cfg_file_path
        )
        self.time_dependent = self.load_cfg_param(
            param_type="TimeDependent", cfg_file_path=cfg_file_path
        )
        self.time_granularity = self.load_cfg_param(
            param_type="TimeGranularity", cfg_file_path=cfg_file_path
        )
        self.space_granularity = self.load_cfg_param(
            param_type="SpaceGranularity", cfg_file_path=cfg_file_path
        )
        self.x_length = self.load_cfg_param(
            param_type="xLength", cfg_file_path=cfg_file_path
        )
        self.y_length = self.load_cfg_param(
            param_type="yLength", cfg_file_path=cfg_file_path
        )
        self.time_horizon = self.load_cfg_param(
            param_type="TimeHorizon", cfg_file_path=cfg_file_path
        )

    def load_cfg_param(self, param_type, cfg_file_path) -> None:
        """Function reading params from xlsx input file."""
        if param_type == "EquationType":
            param = str(
                pd.read_excel(cfg_file_path, usecols="C", skiprows=1, nrows=1).values[
                    0
                ][0]
            )
            return param
        elif param_type == "SolutionScheme":
            param = str(
                pd.read_excel(cfg_file_path, usecols="C", skiprows=2, nrows=1).values[
                    0
                ][0]
            )
            return param
        elif param_type == "TimeDependent":
            param = bool(
                pd.read_excel(cfg_file_path, usecols="C", skiprows=3, nrows=1).values[
                    0
                ][0]
            )
            return param
        elif param_type == "TimeGranularity":
            if bool(self.time_dependent):
                param = float(
                    pd.read_excel(
                        cfg_file_path, usecols="C", skiprows=4, nrows=1
                    ).values[0][0]
                )
            else:
                param = None
            return param
        elif param_type == "SpaceGranularity":
            param = float(
                pd.read_excel(cfg_file_path, usecols="C", skiprows=5, nrows=1).values[
                    0
                ][0]
            )
            return param
        elif param_type == "xLength":
            param = float(
                pd.read_excel(cfg_file_path, usecols="C", skiprows=6, nrows=1).values[
                    0
                ][0]
            )
            return param
        elif param_type == "yLength":
            param = float(
                pd.read_excel(cfg_file_path, usecols="C", skiprows=7, nrows=1).values[
                    0
                ][0]
            )
            return param
        elif param_type == "TimeHorizon":
            if self.time_dependent:
                param = float(
                    pd.read_excel(
                        cfg_file_path, usecols="C", skiprows=8, nrows=1
                    ).values[0][0]
                )
            else:
                param = None
            return param
        return
