import web3
import dotenv

import os

import berakiller.settings


class Berakiller:
    def __init__(self):
        self.connection = get_connection()
        self.wallets = get_wallets()
    
    def balance_is_low(self, address):
        return self.connection.eth.get_balance(address) * berakiller.settings.BERA_DECIMALS > berakiller.settings.LOW_BERA_AMOUNT
    


def get_connection():
    dotenv.load_dotenv()
    return web3.Web3(web3.HTTPProvider(os.environ.get("RPC_URL")))

def get_wallets():
    wallets = list()
    with open("private_keys.txt") as keys_file:
        wallets = keys_file.readlines()
    return wallets
