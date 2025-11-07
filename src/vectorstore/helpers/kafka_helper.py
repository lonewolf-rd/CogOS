from src.vectorstore.utils.config_loader import ConfigLoader
from src.vectorstore.utils.logger import AppLogger



class KafkaHelper:

    def __init__(self):
        self.logger = AppLogger()
        self.config_loader = ConfigLoader()



