import logging

from brainminer.brain import SessionManager, WorldQuantBrain, SimulatorSettings, PerformanceFilter, \
    AlphaSimulationResult
from brainminer.miner.dbwrapper import DbWrapper
from brainminer.miner.schedule import Scheduler
from brainminer.utils import build_alphas
from typing import List, Dict

class AlphaMiner:

    def __init__(self, config_file):
        self._session_manager = SessionManager(config_file)
        self._brain = WorldQuantBrain(self._session_manager)
        self._dbwrapper = DbWrapper(config_file)
        self._scheduler = Scheduler(brain=self._brain, dbwrapper=self._dbwrapper)

    def start_loop(self):
        # start scheduler
        self._scheduler.start_schedule()

    # def mine_alphas(self, batch_name: str, template: str, params: Dict, settings: SimulatorSettings, perf_filter: PerformanceFilter):
    #     # mine alpha based on template
    #     alpha_list = build_alphas(template, params)
    #     logging.info(f"Starting alpha mining, size: {len(alpha_list)}")

    def mine_alphas(self, batch_name: str, template: str, params: Dict, settings: SimulatorSettings):
        # mine alpha based on template
        alpha_list = build_alphas(template, params)
        logging.info(f"Starting alpha mining, size: {len(alpha_list)}")
        # add alpha task
        self._dbwrapper.add_alpha_tasks(batch_name=batch_name, expressions=alpha_list, settings=settings)


if __name__ == "__main__":
    miner = AlphaMiner(config_file=None)
    miner.start_loop()
