import web3
import web3.exceptions

import logging

import modules.utility


class Module:
    def __init__(self, w3: web3.Web3, address: str, abi_path: str) -> None:
        self.w3: web3.Web3 = w3
        self.address: str = address
        self.contract: web3.contract.Contract = modules.utility._get_contract(w3, abi_path, address)

    def _send_tx_and_wait(self, account, tx, message="") -> None:
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
        if tx_receipt.status == 1:
            print(f"Send tx https://bartio.beratrail.io/tx/0x{tx_hash.hex()}")
        else:
            print("пИЗДЕЦ")
            raise Exception