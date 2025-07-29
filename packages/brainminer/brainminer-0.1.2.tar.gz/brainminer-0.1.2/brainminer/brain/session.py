import dataclasses
import logging
import os
import time
import threading
from typing import Optional

import requests
import yaml
from requests.auth import HTTPBasicAuth


@dataclasses.dataclass
class UserCredentials(object):
    user_id: str
    username: str
    password: str

logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s: %(message)s')
logger = logging.getLogger(__name__)

class SessionManager:

    def __init__(self, config_file = None):
        self._sessions = dict()
        self._user: Optional[UserCredentials] = None
        self._session: Optional[requests.Session] = None
        self._last_login_time = 0
        self._lock = threading.Lock()
        self.load_config(config_file)

    def load_config(self, config_file):
        if config_file is None or config_file == '':
            config_file = os.path.expanduser('~/.brain/config.yaml')
        assert os.path.exists(config_file)
        with open(config_file, 'r') as f:
            data = yaml.safe_load(f)
            user_data = data.get('user', {})
            self._user = UserCredentials(**user_data)

    def execute_login(self):
        try:
            self._lock.acquire()
            if self._session is not None:
                return self._session
            cur_thread = threading.current_thread().name
            logger.info(f"Execute login in thread {cur_thread}")
            session = requests.Session()
            session.auth = HTTPBasicAuth(self._user.username, self._user.password)
            resp = session.post('https://api.worldquantbrain.com/authentication')
            if resp.status_code != 201:
                raise Exception(f"Authentication failed: {resp.text}")
            json_resp = resp.json()
            if 'user' in json_resp and 'id' in json_resp['user']:
                assert json_resp['user']['id'] == self._user.user_id
                logger.info("Successfully authenticated with WorldQuant Brain")
                self._last_login_time = time.time()
                self._session = session
            return self._session
        except Exception as e:
            logger.error(f"Execute authentication failed: {str(e)}")
            raise e
        finally:
            self._lock.release()


    def get_session(self) -> Optional[requests.Session]:
        if self._session is None:
            self.execute_login()
        return self._session


    def get(self, url, params=None, headers=None):
        sess = self.get_session()
        resp = sess.get(url, params=params, headers=headers)
        if resp.status_code == 401:
            sess = self.execute_login()
            return sess.get(url, params=params, headers=headers)
        else:
            return resp

    def post(self, url, data=None, json=None, **kwargs):
        sess = self.get_session()
        resp = sess.post(url, data=data, json=json, **kwargs)
        if resp.status_code == 401:
            sess = self.execute_login()
            return sess.post(url, data=data, json=json, **kwargs)
        else:
            return resp

    def patch(self, url, data=None, **kwargs):
        sess = self.get_session()
        resp = sess.patch(url, data=data, **kwargs)
        if resp.status_code == 401:
            sess = self.execute_login()
            return sess.patch(url, data=data, **kwargs)
        else:
            return resp


if __name__ == '__main__':
    m = SessionManager()
    session = m.get_session()
