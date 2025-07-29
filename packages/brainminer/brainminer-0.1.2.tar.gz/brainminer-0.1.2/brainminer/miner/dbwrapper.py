import json
import os
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Type

from brainminer.brain import SimulatorSettings
from brainminer.miner.schema import AlphaTasks
from brainminer.miner.model import AlphaTaskStatus, DBCredentials


class DbWrapper:
    def __init__(self, config_file):
        self._db_info = None
        self.load_config(config_file)
        assert self._db_info is not None
        self._engine = create_engine(self._db_info.to_url())
        self._session = sessionmaker(bind=self._engine)

    def load_config(self, config_file):
        if config_file is None or config_file == '':
            config_file = os.path.expanduser('~/.brain/config.yaml')
        assert os.path.exists(config_file)
        with open(config_file, 'r') as f:
            data = yaml.safe_load(f)
            db_data = data.get('db', {})
            self._db_info = DBCredentials(**db_data)

    def add_alpha_tasks(self, batch_name: str, expressions: List[str], settings: SimulatorSettings):
        tasks = []
        settings_json = json.dumps(settings.config)
        for expression in expressions:
            tasks.append(self.create_alpha_task(batch_name=batch_name, expression=expression, settings=settings_json))
        with self._session() as session:
            session.add_all(tasks)
            session.commit()

    def query_tasks(self, task_status: str, limit: int) -> list[Type[AlphaTasks]]:
        with self._session() as session:
            tasks = session.query(AlphaTasks).filter(AlphaTasks.task_status == task_status).order_by(AlphaTasks.created_at).limit(limit).all()
            return tasks

    def count_task(self, task_status: str) -> int:
        with self._session() as session:
            count = session.query(AlphaTasks).filter(AlphaTasks.task_status == task_status).count()
            return count

    def update_task(self, task: AlphaTasks):
        with self._session() as session:
            session.merge(task)
            session.commit()

    @staticmethod
    def create_alpha_task(batch_name: str, expression: str, settings: str) -> AlphaTasks:
        t = AlphaTasks(batch_name=batch_name, expression=expression, settings=settings)
        t.task_status = AlphaTaskStatus.PENDING.name
        t.simulation_id = ""
        return t


# if __name__ == '__main__':
#     dbwrapper = DbWrapper(config_file=None)
#     dbwrapper.add_alpha_tasks(batch_name="test", expressions=["rank(open - (ts_mean(vwap, 10))) * (-1 * abs(rank(close - vwap)))"], settings=SimulatorSettings())
#     cnt = dbwrapper.count_task(task_status=AlphaTaskStatus.PENDING.name)
#     print(cnt)