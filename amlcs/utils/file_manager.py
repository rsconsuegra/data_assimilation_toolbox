import shutil
import logging
from amlcs import MODEL_PATH

log = logging.getLogger(__name__)


class FileManager:
    def __init__(self, comp_model_path) -> None:
        pass

    @staticmethod
    def create_model_folders(Nens, res_name, comp_model_path) -> None:
        log.info("Creating folders")
        (comp_model_path / "snapshots").mkdir(exist_ok=True)
        ensemble_0 = comp_model_path / "ensemble_0"
        ensemble_0.mkdir(exist_ok=True)
        model_local = comp_model_path / "source_local"
        (comp_model_path / "free_run").mkdir(exist_ok=True)
        (comp_model_path / "initial_condition").mkdir(exist_ok=True)
        (comp_model_path / "model_local").mkdir(exist_ok=True)

        for ensemble in range(Nens):
            (ensemble_0 / f"ens_{ensemble}").mkdir(exist_ok=True)

        log.info("Copying model")
        shutil.copytree(MODEL_PATH / res_name, model_local, dirs_exist_ok=True)

    def clear_model_folders(self) -> None:
        pass
