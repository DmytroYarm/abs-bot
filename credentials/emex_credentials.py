import os

from dotenv import load_dotenv

class EmexCredentials:

    load_dotenv()

    server = os.getenv('OUR_SERVER')
    port = int(os.getenv('OUR_PORT'))
    username = os.getenv('OUR_USERNAME')
    password = os.getenv('OUR_PASSWORD')
    local_path = os.getenv('OUR_LOCAL_PATH')

    emex_server = os.getenv('EMEX_SERVER')
    emex_port = int(os.getenv('EMEX_PORT'))
    emex_username = os.getenv('EMEX_USERNAME')
    emex_password = os.getenv('EMEX_PASSWORD')
    emex_path = os.getenv('EMEX_REMOTE_PASS')


