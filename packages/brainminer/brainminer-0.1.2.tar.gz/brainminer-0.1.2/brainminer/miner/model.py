from enum import Enum

class AlphaTaskStatus(Enum):
    PENDING = 1, # 待调度
    RUNNING = 2, # 运行中
    SUCCESS = 3, # 成功
    FAILED = 4, # 失败


class AlphaSubmitStatus(Enum):
    UNSUBMITTED = 1, # 未提交
    SUBMITTED = 2, # 已提交

class DBCredentials:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def to_url(self):
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

class AlphaTaskInfo:

    def __init__(self, alpha_id: str):
        self.alpha_id = alpha_id
        self.drawdown = None