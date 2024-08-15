import os

from dotenv import load_dotenv

class AutonovaCredentials:

    load_dotenv()

    server = os.getenv('AUTONOVA_SERVER')
    port = int(os.getenv('AUTONOVA_PORT'))
    username = os.getenv('AUTONOVA_USERNAME')
    password = os.getenv('AUTONOVA_PASSWORD')
