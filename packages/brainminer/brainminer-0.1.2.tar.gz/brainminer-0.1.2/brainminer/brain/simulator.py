import json
import logging
import time
from concurrent.futures.thread import ThreadPoolExecutor

from brainminer.brain import SessionManager
from enum import Enum
from typing import List, Optional

from brainminer.brain.model import AlphaSimulationResult
from brainminer.utils import RateLimiter

logger = logging.getLogger(__name__)

class SimulationSubmitResult(object):

    def __init__(self, success: bool, message: str, sim_id: str):
        self.success = success
        self.message = message
        self.sim_id = sim_id

    @staticmethod
    def fail(message: str):
        return SimulationSubmitResult(message=message, success=False, sim_id='')

    @staticmethod
    def success(sim_id: str):
        return SimulationSubmitResult(sim_id=sim_id, success=True, message='Success')

class Universe(Enum):
    TOP3000 = 1
    TOP1000 = 2
    TOP500 = 3
    TOP200 = 4
    TOPSP500 = 5

class Neutralization(Enum):
    NONE = 1
    MARKET = 2
    SECTOR = 3
    INDUSTRY = 4
    SUBINDUSTRY = 5

class SimulatorSettings:

    def __init__(self):
        self._config = {
            'instrumentType': 'EQUITY',
            'region': 'USA',
            'universe': 'TOP3000',
            'delay': 1,
            'decay': 0,
            'neutralization': 'INDUSTRY',
            'truncation': 0.08,
            'pasteurization': 'ON',
            'unitHandling': 'VERIFY',
            'nanHandling': 'OFF',
            'language': 'FASTEXPR',
            'visualization': False,
        }

    @property
    def config(self):
        return self._config

    def set_delay(self, delay: int):
        self._config['delay'] = delay

    def set_decay(self, decay: int):
        self._config['decay'] = decay

    def set_universe(self, uni: Universe):
        self._config['universe'] = uni.name

    def set_neutralization(self, neut: Neutralization):
        self._config['neutralization'] = neut.name

    def update(self, **kwargs):
        self._config.update(kwargs)

    @classmethod
    def from_json(cls, json_str: str):
        settings = cls()
        settings._config = json.loads(json_str)
        return settings

class Simulator:

    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager

    def submit_simulation(self, expression: str, settings: SimulatorSettings = None) -> SimulationSubmitResult:
        """
        submit simulation
        :param expression: fast expression script
        :param settings: simulation settings
        :return: simulation submit result
        """
        if settings is None:
            settings = SimulatorSettings()
        simulation_data = {
            'type': 'REGULAR',
            'settings': settings.config,
            'regular': expression
        }

        while True:
            try:
                logger.info(f"Submitting alpha with expression: {expression}")
                response = self._session_manager.post("https://api.worldquantbrain.com/simulations", json=simulation_data)
                logger.info(f"Response status: {response.status_code}")

                if response.status_code == 201:
                    sim_id = response.headers.get('Location', '').split('/')[-1]
                    if sim_id:
                        logger.info(f"Simulation created with ID: {sim_id}")
                        return SimulationSubmitResult.success(sim_id)
                    else:
                        return SimulationSubmitResult.fail("No simulation ID in response headers")
                elif response.status_code == 400:
                    error_data = response.json()
                    logger.error(f"API error details: {error_data}")
                    error_msg = error_data.get("error", {}).get("message", "Unknown error")
                    return SimulationSubmitResult.fail(error_msg)
                elif response.status_code == 429:
                    retry_after_sec = float(response.headers.get("Retry-After", 0))
                    wait_time = max(retry_after_sec, 10.0)
                    logger.info(f"Rate limited.Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    response.raise_for_status()
                    return SimulationSubmitResult.fail("Unknown error, response = " + response.text)
            except Exception as e:
                logger.error(f"Error testing alpha {expression}: {str(e)}")
                return SimulationSubmitResult.fail(str(e))

    def monitor_simulation(self, sim_id: Optional[str]) -> AlphaSimulationResult:
        """Monitor simulation progress and get final results."""
        if sim_id is None or sim_id == '':
            return AlphaSimulationResult.fail(sim_id='', message="Empty simulation id")
        try:
            sim_data = self.wait_for_simulation_complete(sim_id)
            # If completed, check alpha details
            if sim_data.get("status") in ("COMPLETE", "WARNING") and sim_data.get("alpha"):
                alpha_id = sim_data["alpha"]
            else:
                logger.error(f"Simulation {sim_data.get('status', '')}: {sim_data}")
                return AlphaSimulationResult.fail(sim_id=sim_id, message="Simulation failed,response: " + sim_data)
            logger.info(f"Simulation complete, checking alpha {alpha_id}")
            alpha_data = self.load_alpha_result(alpha_id)
            return AlphaSimulationResult.success(sim_id=sim_id, sim_data=sim_data, alpha_data=alpha_data)
        except Exception as e:
            logger.error(f"Error monitoring simulation {sim_id}: {str(e)}")
            return AlphaSimulationResult.fail(sim_id=sim_id, message=str(e))

    def load_alpha_result(self, alpha_id: str):
        assert alpha_id != ''
        excep = None
        for i in range(3):
            try:
                alpha_response = self._session_manager.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}")
                if alpha_response.status_code == 200:
                    return alpha_response.json()
                else:
                    time.sleep(5)
            except Exception as e:
                excep = e
                time.sleep(5)
        if excep is None:
            raise Exception('Load alpha response fail.')
        else:
            raise excep


    def wait_for_simulation_complete(self, sim_id: str):
        sim_progress_url = f"https://api.worldquantbrain.com/simulations/{sim_id}"
        try:
            while True:
                sim_progres_resp = self._session_manager.get(sim_progress_url)
                sim_data = sim_progres_resp.json()
                if "progress" in sim_data:
                    progress = sim_data.get("progress", 0)
                    logger.info(f"Simulation id: {sim_id}, progress: {progress:.2%}")
                retry_after_sec = float(sim_progres_resp.headers.get("Retry-After", 0))
                # simulation done
                if retry_after_sec == 0:
                    break
                # sleep at least 10 secs
                time.sleep(max(retry_after_sec, 10.0))
            return sim_progres_resp.json()
        except Exception as e:
            logger.error(f"Error testing alpha: {str(e)}")
            raise e

    def execute(self, expression: str, settings: SimulatorSettings = None) -> AlphaSimulationResult:
        if settings is None:
            settings = SimulatorSettings()
        submit_res = self.submit_simulation(expression=expression, settings=settings)
        if submit_res.success:
            return self.monitor_simulation(sim_id=submit_res.sim_id, expression=expression)
        else:
            return AlphaSimulationResult.fail(expr=expression, sim_id = '', message=submit_res.message)

    def execute_multi(self, expression_list: List[str], settings: SimulatorSettings = None, rate_limiter: RateLimiter = None) -> List[AlphaSimulationResult]:
        if settings is None:
            settings = SimulatorSettings()
        if rate_limiter is None:
            rate_limiter = RateLimiter()
        logging.info(f"Starting batch simulation of {len(expression_list)} alphas")
        alpha_results: List[AlphaSimulationResult] = []
        with ThreadPoolExecutor(max_workers = 4) as executor:
            futures = []
            for expression in expression_list:
                rate_limiter.wait_for_slot()
                future = executor.submit(self.execute, expression=expression, settings=settings)
                futures.append(future)
            # process results and set up monitoring
            for future in futures:
                try:
                    alpha_result = future.result()
                    if alpha_result:
                        alpha_results.append(alpha_result)
                except Exception as e:
                    logging.error(f"Error in simulating alpha: {str(e)}")
            return alpha_results

if __name__ == '__main__':
    s = Simulator(session_manager=SessionManager())
    res = s.load_alpha_result(alpha_id='r7kWAXo')
    print(json.dumps(res))
    # periods = [10, 20, 33, 66]
    # text_exprs = []
    # for period in periods:
    #     expr = f"rank(open - (ts_mean(vwap, {period}))) * (-1 * abs(rank(close - vwap)))"
    #     print(expr)
    #     text_exprs.append(expr)
    # for period in periods:
    #     expr = f"rank(open - (ts_mean(close, {period}))) * (-1 * abs(rank(open - vwap)))"
    #     text_exprs.append(expr)
    # res = s.execute_multi(expression_list=text_exprs)
    # print(json.dumps(res))


