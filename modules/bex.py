import json
import requests

import web3

class Bex:
    def __init__(self, connection):
        self.connection = connection
        self.address = "0x21e2C0AFd058A89FCf7caf3aEA3cB84Ae977B73D"
        abi_file = open("abis/bex/BeraCrocMultiSwap.json")
        abi = json.load(abi_file)
        abi_file.close()
        self.contract = self.connection.eth.contract(address=self.address, abi=abi)
        

    def swap(self, account):
        amount = 97358700000000
        wbera_address = "0x7507c1dc16935B82698e4C63f2746A2fCf994dF8"
        usdc_address = "0xE28AfD8c634946833e89ee3F122C06d7C537E8A8"

        wbera_abi_file = open("abis/core/WBERA.json")
        wbera_abi = json.load(wbera_abi_file)
        wbera_abi_file.close()
        wbera_contract = self.connection.eth.contract(address="0x7507c1dc16935B82698e4C63f2746A2fCf994dF8", abi=wbera_abi)
        tx = wbera_contract.functions.approve("0x21e2C0AFd058A89FCf7caf3aEA3cB84Ae977B73D", amount).build_transaction({
            'from': account.address,
            'nonce': self.connection.eth.get_transaction_count(account.address),
            'gas': 500000,
            'maxFeePerGas': 200000000,
            'maxPriorityFeePerGas': 100000000,
        })
        signed_tx = self.connection.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = self.connection.eth.send_raw_transaction(signed_tx.raw_transaction)
        print("Approved - ", tx_hash.hex())
        tx_receipt = self.connection.eth.wait_for_transaction_receipt(tx_hash)

        router_api = "https://bartio-bex-router.berachain-devnet.com/dex/route?fromAsset=0x7507c1dc16935B82698e4C63f2746A2fCf994dF8&toAsset=0xE28AfD8c634946833e89ee3F122C06d7C537E8A8&amount=97358700000000"
        resp = requests.get(router_api).json()
        print(resp)
        steps = [(
            int(step["poolIdx"]), 
            self.connection.to_checksum_address(step["base"]), 
            self.connection.to_checksum_address(step["quote"]), 
            step["isBuy"]
        ) for step in resp["steps"]]
        tx = self.contract.functions.multiSwap(steps, 97358700000000, 1000).build_transaction({
            "from": account.address,
            "nonce": self.connection.eth.get_transaction_count(account.address),
            'gas': 500000,
            'maxFeePerGas': 200000000,
            'maxPriorityFeePerGas': 100000000,
        })
        signed_tx = self.connection.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = self.connection.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Swapped - 0x{tx_hash.hex()}")

    
    def add_liquidity(self):
        ...