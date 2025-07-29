from typing import List, Dict

from brainminer.brain.model import AlphaAggregateData, AlphaSimulationResult, PerformanceFilter


class Evaluator:

    @staticmethod
    def get_fitness_level(fitness: float, delay: int):
        if delay == 0:
            if fitness > 3.25:
                return 'Spectacular'
            elif fitness > 2.6:
                return 'Excellent'
            elif fitness > 1.95:
                return 'Good'
            elif fitness > 1.3:
                return 'Average'
            else:
                return 'Needs Improvement'
        else:
            if fitness > 2.5:
                return 'Spectacular'
            elif fitness > 2:
                return 'Excellent'
            elif fitness > 1.5:
                return 'Good'
            elif fitness > 1:
                return 'Average'
            else:
                return 'Needs Improvement'

    @staticmethod
    def get_is_metrics(alpha_data: Dict):
        return alpha_data['is']

    @staticmethod
    def extract_aggregate_data(alpha_data: Dict) -> AlphaAggregateData:
        metrics = alpha_data['is']
        data = AlphaAggregateData(alpha_id=alpha_data['id'])
        data.extract_metrics(metrics)
        return data

    @staticmethod
    def load_is_fail_checks(alpha_data: Dict) -> List[str]:
        is_metrics = alpha_data['is']
        fail_checks = []
        for item in is_metrics['checks']:
            if item['result'] == 'FAIL':
                reason = "{}:{} is below cutoff of {}".format(item['name'], item["value"], item["limit"])
                fail_checks.append(reason)
        return fail_checks

    @staticmethod
    def filter_alphas(alpha_result: List[AlphaSimulationResult], perf_filter: PerformanceFilter) -> List[str]:
        match_alphas = []
        for item in alpha_result:
            if item.success and item.alpha_data is not None and perf_filter.is_match(item.alpha_data['is']):
                match_alphas.append(item.alpha_data['id'])
        return match_alphas



