import json
import logging
import os
import time

from brainminer.brain.session import SessionManager
from brainminer.brain.model import PerformanceFilter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict

# Configure logger
logger = logging.getLogger(__name__)

class AlphaManager:

    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager

    # def filter_alphas(self, perf_filter: PerformanceFilter) -> List[str]:
    #     match_alphas = []
    #     for item in alpha_result:
    #         if item.success and item.alpha_data is not None and perf_filter.is_match(item.alpha_data['is']):
    #             match_alphas.append(item.alpha_data['id'])
    #     return match_alphas

    def fet_successful_alphas(self, offset: int = 0, limit: int = 10):
        """Fetch successful unsubmitted alphas with good performance metrics."""
        url = "https://api.worldquantbrain.com/users/self/alphas"
        params = {
            "limit": limit,
            "offset": offset,
            "status": "UNSUBMITTED",
            "is.fitness>": 1,
            "is.sharpe>": 1.25,
            "order": "-dateCreated",
            "hidden": "false"
        }
        logger.info(f"Fetching alphas with params: {params}")
        full_url = f"{url}?{'&'.join(f'{k}={v}' for k,v in params.items())}"
        logger.info(f"Request URL: {full_url}")

        max_retries = 3
        retry_delay = 60
        for attempt in range(max_retries):
            try:
                logger.debug(f"Attempt {attempt + 1}/{max_retries} to fetch alphas")
                response = self._session_manager.get(url, params=params)
                logger.info(f"Response URL: {response.url}")
                logger.info(f"Response status: {response.status_code}")
                logger.info(f"Response headers: {dict(response.headers)}")
                logger.info(f"Response content: {response.text[:1000]}...")  # First 1000 chars

                if response.status_code == 429:  # Too Many Requests
                    wait_time = int(response.headers.get('Retry-After', retry_delay))
                    logger.info(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                data = response.json()
                logger.info(
                    f"Successfully fetched {len(data.get('results', []))} alphas. Total count: {data.get('count', 0)}")
                return data

            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    logger.warning(f"Response URL: {response.url if 'response' in locals() else 'N/A'}")
                    logger.warning(f"Response text: {response.text if 'response' in locals() else 'N/A'}")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"Failed to fetch alphas after {max_retries} attempts. Last error: {e}")
                    logger.error(f"Last response URL: {response.url if 'response' in locals() else 'N/A'}")
                    logger.error(f"Last response text: {response.text if 'response' in locals() else 'N/A'}")
                    return {"count": 0, "results": []}

        return {"count": 0, "results": []}

    def monitor_submission(self, alpha_id: str, max_attempts: int = 30, sleep_time: int = 10) -> Dict:
        """Monitor submission status until complete or failed."""
        url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/submit"

        for attempt in range(max_attempts):
            try:
                response = self.sess.get(url)
                logger.info(f"Monitoring attempt {attempt + 1} for alpha {alpha_id}")
                logger.info(f"Response status: {response.status_code}")
                logger.info(f"Response content: {response.text[:1000]}...")

                if response.status_code != 200:
                    logger.error(f"Submission likely failed for alpha {alpha_id}")
                    logger.error(f"Response status: {response.status_code}")
                    logger.error(f"Response text: {response.text}")
                    return {"status": "failed", "error": response.text}

                # If response is empty (still submitting)
                if not response.text.strip():
                    logger.info(f"Alpha {alpha_id} still being submitted, waiting...")
                    time.sleep(sleep_time)
                    continue

                # Try to parse JSON response (submission complete)
                try:
                    data = response.json()
                    logger.info(f"Submission complete for alpha {alpha_id}")
                    return data
                except json.JSONDecodeError:
                    logger.info(f"Response not in JSON format yet for alpha {alpha_id}, continuing to monitor...")

            except Exception as e:
                logger.warning(f"Monitor attempt {attempt + 1} failed: {str(e)}")
                logger.warning(f"Response content: {response.text if 'response' in locals() else 'N/A'}")

            time.sleep(sleep_time)

        logger.error(f"Monitoring timed out for alpha {alpha_id}")
        return {"status": "timeout", "error": "Monitoring timed out"}

    def log_submission_result(self, alpha_id: str, result: Dict) -> None:
        """Log submission result to file."""
        log_file = 'submission_results.json'

        # Load existing results
        existing_results = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    existing_results = json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Could not parse {log_file}, starting fresh")

        # Add new result
        entry = {
            "alpha_id": alpha_id,
            "timestamp": int(time.time()),
            "result": result
        }
        existing_results.append(entry)

        # Save updated results
        with open(log_file, 'w') as f:
            json.dump(existing_results, f, indent=2)

        logger.info(f"Logged submission result for alpha {alpha_id}")

    def has_fail_checks(self, alpha: Dict) -> bool:
        """Check if alpha has any FAIL results in checks."""
        checks = alpha.get("is", {}).get("checks", [])
        return any(check.get("result") == "FAIL" for check in checks)

    def submit_alpha(self, alpha_id: str) -> bool:
        """Submit a single alpha and monitor its status."""
        url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/submit"
        logger.info(f"Submitting alpha {alpha_id}")
        logger.info(f"Request URL: {url}")

        try:
            # Initial submission
            response = self.sess.post(url)
            logger.info(f"Response status: {response.status_code}")

            if response.status_code == 201:
                logger.info(f"Successfully submitted alpha {alpha_id}, monitoring status...")

                # Monitor submission status
                result = self.monitor_submission(alpha_id)
                if result:
                    self.log_submission_result(alpha_id, result)
                    return True
                else:
                    logger.error(f"Submission monitoring timed out for alpha {alpha_id}")
                    return False
            else:
                logger.error(f"Failed to submit alpha {alpha_id}. Status: {response.status_code}")
                logger.error(f"Response text: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error submitting alpha {alpha_id}: {str(e)}")
            logger.exception("Full traceback:")
            return False

    def batch_submit(self, batch_size: int = 5) -> None:
        """Submit alphas in batches with pagination."""
        logger.info(f"Starting batch submission with batch size {batch_size}")
        offset = 0
        total_submitted = 0

        while True:
            logger.info(f"Fetching batch at offset {offset}")
            response = self.fetch_successful_alphas(offset=offset, limit=batch_size)

            if not response or not response.get("results"):
                logger.info("No more alphas to process")
                break

            results = response["results"]
            if not results:
                logger.info("Empty results batch")
                break

            logger.info(f"Processing batch of {len(results)} alphas...")

            # Filter out alphas with FAIL checks
            valid_alphas = [alpha for alpha in results if not self.has_fail_checks(alpha)]
            logger.info(f"Found {len(valid_alphas)} valid alphas after filtering FAILs")

            if not valid_alphas:
                logger.info("No valid alphas in this batch, moving to next")
                offset += batch_size
                continue

            # Submit valid alphas in parallel
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                for alpha in valid_alphas:
                    alpha_id = alpha["id"]
                    expression = alpha["regular"]["code"]
                    metrics = (f"Sharpe: {alpha['is']['sharpe']}, "
                               f"Fitness: {alpha['is']['fitness']}")
                    logger.info(f"Queuing alpha {alpha_id} for submission:")
                    logger.info(f"Expression: {expression}")
                    logger.info(f"Metrics: {metrics}")
                    futures.append(executor.submit(self.submit_alpha, alpha_id))

                for future in as_completed(futures):
                    if future.result():
                        total_submitted += 1

            if not response.get("next"):
                logger.info("No more pages to process")
                break

            offset += batch_size
            logger.info(f"Waiting 60 seconds before next batch...")
            time.sleep(60)

        logger.info(f"Submission process complete. Total alphas submitted: {total_submitted}")
