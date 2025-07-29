import dataclasses

from brainminer.utils import is_empty_metrics
from typing import Any

@dataclasses.dataclass
class AlphaAggregateData:

    def __init__(self, alpha_id: str):
        self.alpha_id = alpha_id
        self.drawdown = None
        self.turnover = None
        self.sharpe = None
        self.margin = None
        self.fitness = None
        self.returns = None

    def extract_metrics(self, metrics):
        self.sharpe = metrics['sharpe']
        self.turnover = metrics['turnover']
        self.drawdown = metrics['drawdown']
        self.margin = metrics['margin']
        self.fitness = metrics['fitness']
        self.returns = metrics['returns']

class PerformanceFilter:

    def __init__(self, fitness = 1.0, sharpe = 1.25, turnover = -1.0, drawdown = -1.0, returns = 0.2):
        self._fitness = fitness
        self._sharpe = sharpe
        self._turnover = turnover
        self._drawdown = drawdown
        self._returns = returns

    @property
    def fitness(self):
        return self._fitness

    @property
    def sharpe(self):
        return self._sharpe

    @property
    def turnover(self):
        return self._turnover

    @property
    def drawdown(self):
        return self._drawdown

    @property
    def returns(self):
        return self._returns

    def is_match(self, metrics) -> bool:
        if self._fitness > 0.0 and metrics['fitness'] < self._fitness:
            return False
        if self._sharpe > 0.0 and metrics['sharpe'] < self._sharpe:
            return False
        if 0.0 < self._turnover < metrics['turnover']:
            return False
        if 0.0 < self._drawdown < metrics['drawdown']:
            return False
        if self._returns > 0.0 and metrics['returns'] < self._returns:
            return False
        return True


class AlphaSimulationResult:

    def __init__(self, success: bool, message: str, sim_id: str, sim_data: Any, alpha_data: Any):
        self.success = success
        self.message = message
        self.sim_id = sim_id
        self.sim_data = sim_data
        self.alpha_data = alpha_data

    @staticmethod
    def fail(sim_id: str, message: str):
        return AlphaSimulationResult(success=False, sim_id=sim_id, message=message, sim_data=None,
                                     alpha_data=None)

    @staticmethod
    def success(sim_id: str, sim_data: Any, alpha_data: Any):
        return AlphaSimulationResult(success=True, sim_id=sim_id, message='', sim_data=sim_data,
                                     alpha_data=alpha_data)

    def get_alpha_id(self):
        return '' if self.alpha_data is None else self.alpha_data['id']

    def is_match(self, perf_filter: PerformanceFilter):
        if self.success and self.alpha_data is not None:
            m = perf_filter.is_match(self.alpha_data['is'])
            if not m:
                return False
            if not is_empty_metrics(self.alpha_data['os']):
                return perf_filter.is_match(self.alpha_data['os'])
        return False

