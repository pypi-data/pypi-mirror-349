import logging
import pandas as pd

from brainminer.brain import Simulator, SessionManager, AlphaManager, SimulatorSettings, AlphaSimulationResult
from brainminer.brain.simulator import SimulationSubmitResult
from brainminer.utils import RateLimiter
from typing import List, Dict

logger = logging.getLogger(__name__)

class WorldQuantBrain:

    def __init__(self, session_manager: SessionManager = None):
        if session_manager is None:
            session_manager = SessionManager()
        self._session_manager = session_manager
        self._simulator = Simulator(session_manager=session_manager)
        self._alpha_submitter = AlphaManager(session_manager=session_manager)

    def submit_simulation(self, expr: str, settings: SimulatorSettings = None) -> SimulationSubmitResult:
        return self._simulator.submit_simulation(expression=expr, settings=settings)

    def execute_simulation(self, expr: str, settings: SimulatorSettings = None) -> AlphaSimulationResult:
        return self._simulator.execute(expression=expr, settings=settings)

    def execute_multi_simulation(self, expression_list: List[str], settings: SimulatorSettings = None, rate_limiter: RateLimiter = None) -> List[AlphaSimulationResult]:
        return self._simulator.execute_multi(expression_list=expression_list, settings=settings, rate_limiter=rate_limiter)

    def monitor_simulation(self, sim_id: str) -> AlphaSimulationResult:
        return self._simulator.monitor_simulation(sim_id)

    def load_alpha_result(self, alpha_id: str):
        return self._simulator.load_alpha_result(alpha_id)

    def get_operators(self) -> List[Dict]:
        """Fetch available operators from WorldQuant Brain."""
        try:
            print("Requesting operators...")
            response = self._session_manager.get('https://api.worldquantbrain.com/operators')

            response.raise_for_status()
            data = response.json()

            # Handle different response formats
            if isinstance(data, list):
                return data
            return data.get('results', [])
        except Exception as e:
            logger.error(f"Failed to fetch operators: {e}")
            return []

    def set_alpha_properties(self,
                             alpha_id,
                             name: str = None,
                             color: str = None,
                             selection_desc: str = "None",
                             combo_desc: str = "None",
                             tags: List = None,
                             ):
        """
        Function changes alpha's description parameters
        """

        if tags is None:
            tags = []
        params = {
            "color": color,
            "name": name,
            "tags": tags,
            "category": None,
            "regular": {"description": None},
            "combo": {"description": combo_desc},
            "selection": {"description": selection_desc},
        }
        response = self._session_manager.patch(
            "https://api.worldquantbrain.com/alphas/" + alpha_id, json=params
        )

    def get_datafields(self,instrument_type: str = 'EQUITY',
                       region: str = 'USA', delay: int = 1,
                       universe: str = 'TOP3000', dataset_id: str = '', search: str = '') -> pd.DataFrame:
        """
        get available datafields
        data columns: id | description | dataset | category | subcategory | region | delay | universe | type | coverage | userCount | alphaCount | themes |
        """
        if len(search) == 0:
            url_template = "https://api.worldquantbrain.com/data-fields?" +\
                f"&instrumentType={instrument_type}" +\
                f"&region={region}&delay={str(delay)}&universe={universe}&dataset.id={dataset_id}&limit=50" +\
                "&offset={x}"
            count = self._session_manager.get(url_template.format(x=0)).json()['count']
        else:
            url_template = "https://api.worldquantbrain.com/data-fields?" +\
                f"&instrumentType={instrument_type}" +\
                f"&region={region}&delay={str(delay)}&universe={universe}&limit=50" +\
                f"&search={search}" +\
                "&offset={x}"
            count = 100

        datafields_list = []
        for x in range(0, count, 50):
            url = url_template.format(x=x)
            datafields = self._session_manager.get(url)
            datafields_list.append(datafields.json()['results'])

        datafields_list_flat = [item for sublist in datafields_list for item in sublist]

        datafields_df = pd.DataFrame(datafields_list_flat)
        return datafields_df

# if __name__ == '__main__':
#     brain = WorldQuantBrain()
#     res = brain.load_alpha_result(alpha_id='1NMg3dz')
#     print(res)