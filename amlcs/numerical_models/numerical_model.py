class NumericalModel():
    def __init__(self, model_cfg, res_name) -> None:
        self.model_resolution = model_cfg.get(res_name)
        self.variables_layers = model_cfg.get("variables")

    def set_time_integration(self, args):
        nmonths = args[0]
        days = args[1]
        restart = args[2]
        self.create_cls_instep_file(nmonths, days, restart)
        self.create_cls_indyns_file()
        os.system(
            f"mv cls_instep.h {self.source_local}cls_instep.h; mv cls_indyns.h {self.source_local}cls_indyns.h; cd {self.source_local}/ ; sh compile.sh>out.txt;"
        )
