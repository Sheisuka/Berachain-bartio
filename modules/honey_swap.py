import web3

import settings
import modules.module
import modules.utility
import modules.handlers


class HoneySwap(modules.module.Module):
    def __init__(self, w3: web3.Web3):
        super().__init__(w3, settings.DAPPS["HONEYSWAP"]["ADDRESS"], settings.DAPPS["HONEYSWAP"]["ABI_PATH"])

    def mint_honey(self, account: web3.Account, base: str, amount: int) -> None:        
        self._approve(account, base, amount)
        self._mint_honey(account, base, amount)

    def reedem_for_honey(self, account: web3.Account, quote: str, amount: int) -> None:
        self._approve(account, quote, amount)
        self._redeem_for_honey(account, quote, amount)
    
    def _mint_honey(self, account: web3.Account, base: str, amount: int) -> None:
        tx = self.contract.functions.mint(base, amount, account.address).build_transaction({
            'gas': 500000,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'maxFeePerGas': 200000000,
            'maxPriorityFeePerGas': 100000000,
        })
        self._send_tx_and_wait(account, tx)
    
    def _redeem_for_honey(self, account: web3.Account, quote: str, amount: int) -> None:
        tx = self.contract.functions.redeem(quote, amount, account.address).build_transaction({
            'gas': 500000,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'maxFeePerGas': 200000000,
            'maxPriorityFeePerGas': 100000000,
        })
        self._send_tx_and_wait(account, tx)