import web3
import web3.contract
import web3.eth
import web3.exceptions

import settings
import modules.handlers
import modules.utility


class Module:
    def __init__(self, w3: web3.Web3, address: str, abi_path: str) -> None:
        self.w3: web3.Web3 = w3
        self.address: str = address
        self.contract: web3.contract.Contract = modules.utility._get_contract(w3, address, abi_path)

    @modules.handlers.exception_handler
    def _send_tx_and_wait(self, account: web3.Account, tx, message: str = "") -> None:
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
        if tx_receipt.status == 1:
            print(f"Send tx https://bartio.beratrail.io/tx/0x{tx_hash.hex()}")
        else:
            print("Some error")
            raise Exception
    
    def _approve(self, account: web3.Account, asset: str, amount: int, address: str) -> None:
        contract = modules.utility._get_contract(self.w3, asset, settings.TOKENS[asset]["ABI_PATH"])
        if contract.functions.allowance(account.address, address).call() >= amount:
            return
        tx = contract.functions.approve(address, amount).build_transaction({
            'gas': 500000,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'maxFeePerGas': 200000000,
            'maxPriorityFeePerGas': 100000000,
        })
        self._send_tx_and_wait(account, tx)