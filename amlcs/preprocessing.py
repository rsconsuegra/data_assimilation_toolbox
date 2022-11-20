import logging
from pathlib import Path
from typing import Dict

import hydra
from omegaconf import DictConfig, OmegaConf

from amlcs import RESULTS_FOLDER
from amlcs.utils.file_manager import FileManager as FM

log = logging.getLogger(__name__)


@hydra.main(version_base="1.2", config_path="conf", config_name="conf_pre")
def main(cfg: DictConfig) -> None:
    prepro = Preprocessing(cfg)
    prepro.create_model_folder()
    prepro.set_numerical_model()


class Preprocessing:
    """
    Class that defines the Data Assimilatio Pre-Processing for the model
    """

    def __init__(self, cfg) -> None:
        self.exe_model_path: Path = None
        self.cfg: DictConfig = cfg.pre
        self.res: Dict = cfg.model_res.get(self.cfg.res_name)
        self.FM = FM()
        log.info(f"{self.cfg.res_name.upper()} resolution will be used")
        log.info("Parameters: %s", OmegaConf.to_yaml(self.cfg))

    def create_model_folder(self) -> None:
        if self.cfg.code:
            code_path: str = self.cfg.code
        else:
            res_ens = f"{self.cfg.res_name}_{self.cfg.Nens}"
            per_m = f"{self.cfg.per}_{self.cfg.M}"
            code_path: str = f"{res_ens}_{per_m}"

        path: str = f"{self.cfg.folder_prep}/{code_path}"
        self.exe_model_path = RESULTS_FOLDER / path
        self.exe_model_path.mkdir(parents=True, exist_ok=True)
        log.info(f"{self.exe_model_path} folder created")

    def set_numerical_model(self) -> None:
        FM.create_model_folders(self.cfg.Nens, self.cfg.res_name, self.exe_model_path)


if __name__ == "__main__":
    main()
