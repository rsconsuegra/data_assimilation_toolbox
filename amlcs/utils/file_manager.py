import shutil
import logging
from amlcs import MODEL_PATH

log = logging.getLogger(__name__)


class FileManager:
    def __init__(self, comp_model_path) -> None:
        self.snapshots = comp_model_path / "snapshots"
        self.ensemble_0 = comp_model_path / "ensemble_0"
        self.source_model_local = comp_model_path / "source_local"
        self.free_run = comp_model_path / "free_run"
        self.init_cond = comp_model_path / "initial_condition"
        self.model_local = comp_model_path / "model_local"

    def create_model_folders(self, Nens, res_name) -> None:
        log.info("Creating folders")
        self.snapshots.mkdir(exist_ok=True)
        self.ensemble_0.mkdir(exist_ok=True)
        self.free_run.mkdir(exist_ok=True)
        self.init_cond.mkdir(exist_ok=True)
        self.model_local.mkdir(exist_ok=True)

        for ensemble in range(Nens):
            (self.ensemble_0 / f"ens_{ensemble}").mkdir(exist_ok=True)

        log.info("Copying model")
        res_model = MODEL_PATH / res_name
        shutil.copytree(res_model, self.source_model_local, dirs_exist_ok=True)

    def clear_model_folders(self) -> None:
        shutil.rmtree(self.ensemble_0)
        shutil.rmtree(self.source_model_local)
        shutil.rmtree(self.model_local)
