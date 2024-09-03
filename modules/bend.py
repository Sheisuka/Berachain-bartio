import web3
import web3.contract

import settings
import modules.handlers
import modules.module
import modules.utility


class Bend(modules.module.Module):
    def __init__(self, w3: web3.contract.Contract) -> None:
        super().__init__(w3, settings.DAPPS["BEND"]["ADDRESS"], settings.DAPPS["BEND"]["ABI_PATH"])
        self.refferal_code = 0 # no refferer
        self.interest_rate_mode = 1 # stable
    
    def supply(self, account: web3.Account, asset: str, amount: int) -> None:
        self._approve(account, asset, amount)
        self._supply(account, asset, amount)
    
    def withdraw(self, account: web3.Account, asset: str, amount: int) -> None:
        self._withdraw(account, asset, amount)
    
    def borrow(self, account: web3.Account, asset: str, amount: int) -> None:
        self._borrow(account, asset, amount)
    
    def repay(self, account: web3.Account, asset: str, amount: int) -> None:
        self._approve(account, asset, amount)
        self._repay(account, asset, amount)
    
    def _supply(self, account: web3.Account, asset: str, amount: int) -> None:
        tx = self.contract.functions.supply(asset, amount, account.address, self.refferal_code).build_transaction({
            'gas': 500000,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'maxFeePerGas': 200000000,
            'maxPriorityFeePerGas': 100000000,
        })
        self._send_tx_and_wait(account, tx)
    
    def _withdraw(self, account: web3.Account, asset: str, amount: int) -> None:
        tx = self.contract.functions.withdraw(asset, amount, account.address).build_transaction({
            'gas': 500000,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'maxFeePerGas': 200000000,
            'maxPriorityFeePerGas': 100000000,
        })
        self._send_tx_and_wait(account, tx)
    
    def _borrow(self, account: web3.Account, asset: str, amount: int) -> None:
        user_data = self.contract.functions.getUserAccountData(account.address).call()
        borrowing_power_left = user_data[2]
        if amount > borrowing_power_left:
            amount = borrowing_power_left

        tx = self.contract.functions.borrow(asset, amount, self.interest_rate_mode, self.refferal_code, account.address).build_transaction({
            'gas': 500000,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'maxFeePerGas': 200000000,
            'maxPriorityFeePerGas': 100000000,
        })
        self._send_tx_and_wait(account, tx)

    def _repay(self, account: web3.Account, asset: str, amount: int) -> None:
        tx = self.contract.functions.repay(asset, amount, self.interest_rate_mode, account.address).build_transaction({
            'gas': 500000,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'maxFeePerGas': 200000000,
            'maxPriorityFeePerGas': 100000000,
        })
        self._send_tx_and_wait(account, tx)