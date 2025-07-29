import json
import logging
import threading

from brainminer.miner.dbwrapper import DbWrapper
from brainminer.miner.model import AlphaSubmitStatus, AlphaTaskStatus
from brainminer.miner.schema import AlphaTasks
from brainminer.brain import AlphaSimulationResult, SimulatorSettings, SimulationSubmitResult, WorldQuantBrain
from brainminer.utils import json_to_class
from datetime import datetime
from typing import Type

logger = logging.getLogger(__name__)

class Scheduler():

    def __init__(self, brain: WorldQuantBrain, dbwrapper: DbWrapper):
        self._brain = brain
        self._timer = threading.Timer(1, self.do_schedule)
        self._db = dbwrapper

    def do_schedule(self):
        # 查询待调度的任务，一次最多使用3个
        cnt = self._db.count_task(task_status=AlphaTaskStatus.RUNNING.name)
        if cnt > 3:
            logger.info(f"Current running task count = {cnt}, skip submit simulation.")
        else:
            pending_tasks = self._db.query_tasks(task_status=AlphaTaskStatus.PENDING.name, limit=3-cnt)
            for task in pending_tasks:
                logger.info(f"Submit alpha to do simulation, batch name = {task.batch_name}.")
                self.submit_simulation(task)

        # 查询未完成的任务
        running_tasks = self._db.query_tasks(task_status=AlphaTaskStatus.RUNNING.name, limit=3)
        if len(running_tasks) > 0:
            for task in running_tasks:
                logger.info(f"Check alpha simulation result, simulation id = {task.simulation_id}")
                self.check_simulation_result(task)
        else:
            logger.info("No running task found.")

        self._timer = threading.Timer(10, self.do_schedule)
        self._timer.start()

    @staticmethod
    def parse_alpha_result(task: Type[AlphaTasks], alpha_data):
        is_result = alpha_data['is']
        os_result = alpha_data['os']
        if is_result is not None:
            task.is_sharpe = is_result.get('sharpe')
            task.is_returns = is_result.get('returns')
            task.is_turnover = is_result.get('turnover')
            task.is_fitness = is_result.get('fitness')
            task.is_drawdown = is_result.get('drawdown')
        if os_result is not None:
            task.os_sharpe = os_result.get('sharpe')
            task.os_returns = os_result.get('returns')
            task.os_turnover = os_result.get('turnover')
            task.os_fitness = os_result.get('fitness')
            task.os_drawdown = os_result.get('drawdown')
        task.evaluation_level = alpha_data.get('grade')

    def check_simulation_result(self, task: Type[AlphaTasks]):
        res: AlphaSimulationResult = self._brain.monitor_simulation(task.simulation_id)
        if res.success:
            task.task_status = AlphaTaskStatus.SUCCESS.name
            task.updated_at = datetime.now()
            task.alpha_id = res.sim_data["alpha"]
            task.submit_status = AlphaSubmitStatus.UNSUBMITTED.name
            task.alpha_result = json.dumps(res.alpha_data)
            self.parse_alpha_result(task, res.alpha_data)
            self._db.update_task(task)
        else:
            task.task_status = AlphaTaskStatus.FAILED.name
            task.updated_at = datetime.now()
            logger.error(f"Check simulation result failed, message = {res.message}, expression={task.expression}")
            self._db.update_task(task)

    def submit_simulation(self, task: Type[AlphaTasks]):
        settings = SimulatorSettings.from_json(task.settings)
        res: SimulationSubmitResult = self._brain.submit_simulation(task.expression, settings)
        if res.success:
            task.task_status = AlphaTaskStatus.RUNNING.name
            task.updated_at = datetime.now()
            task.simulation_id = res.sim_id
            self._db.update_task(task)
        else:
            task.task_status = AlphaTaskStatus.FAILED.name
            task.updated_at = datetime.now()
            logger.error(f"Submit simulation failed, message = {res.message}, expression={task.expression}")
            self._db.update_task(task)

    def start_schedule(self):
        self._timer.start()

    def stop_schedule(self):
        self._timer.cancel()