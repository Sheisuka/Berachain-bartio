import json


class HoneySwap:
    def __init__(self, connection):
        self.connection = connection
        self.address = "0xAd1782b2a7020631249031618fB1Bd09CD926b31"
        honey_factory_abi_file = open("berakiller/abis/core/HoneyFactory.json")
        honey_factory_abi = json.load(honey_factory_abi_file)
        honey_factory_abi_file.close()
        self.contract = connection.eth.contract(address=self.address, abi=honey_factory_abi)

    def mint(self, account, asset, amount):
        from_ = account.address

        nonce = self.connection.eth.get_transaction_count(from_)
        usdc_abi_file = open("berakiller/abis/core/USDC.json")
        usdc_abi = json.load(usdc_abi_file)
        usdc_abi_file.close()
        usdc_contract = self.connection.eth.contract(address="0xd6D83aF58a19Cd14eF3CF6fe848C9A4d21e5727c", abi=usdc_abi)
        tx = usdc_contract.functions.approve(self.address, amount).build_transaction({
            'from': from_,
            'nonce': nonce,
            'gas': 500000,
            'maxFeePerGas': 200000000,
            'maxPriorityFeePerGas': 100000000,
        })
        signed_tx = self.connection.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = self.connection.eth.send_raw_transaction(signed_tx.raw_transaction)
        print("Approved - ", tx_hash.hex())
        tx_receipt = self.connection.eth.wait_for_transaction_receipt(tx_hash)

        nonce = self.connection.eth.get_transaction_count(from_)
        tx = self.contract.functions.mint(asset, amount, from_).build_transaction({
            'from': from_,
            'nonce': nonce,
            'gas': 500000,
            'maxFeePerGas': 200000000,
            'maxPriorityFeePerGas': 100000000,
        })
        signed_tx = self.connection.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = self.connection.eth.send_raw_transaction(signed_tx.raw_transaction)
        print("Minted - ", tx_hash.hex())

    def reedem(self):
        ...