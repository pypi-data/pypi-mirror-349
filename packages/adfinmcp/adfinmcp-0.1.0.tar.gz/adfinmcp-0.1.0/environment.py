import os

from dotenv import load_dotenv

load_dotenv()

def get_sensitive_data():
    return {
        'adfin email': Environment.get('ADFIN_EMAIL'),
        'adfin password': Environment.get('ADFIN_PASSWORD'),
        'actionstep email': Environment.get('ACTIONSTEP_USERNAME'),
        'actionstep password': Environment.get('ACTIONSTEP_PASSWORD'),
    }

class Environment:
    @staticmethod
    def get(__key, __default=None):
        return os.getenv(__key, __default)

    __getattr__ = dict.get
