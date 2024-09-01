import web3

import requests

import settings
import modules.module
import modules.utility
import modules.handlers


class Bex(modules.module.Module):
    def __init__(self, w3):
        super().__init__(w3, settings.DAPPS["BEX"]["ADDRESS"], settings.DAPPS["BEX"]["ABI_PATH"])

    def swap(self, account: web3.Account, asset_from: str, asset_to: str, amount: int = 973587000000000):
        @modules.handlers.exception_handler
        def _approve():
            from_contract = modules.utility._get_contract(self.w3, settings.TOKENS[asset_from]["ABI_PATH"], settings.TOKENS[asset_from]["ADDRESS"])
            if from_contract.functions.allowance(account.address, self.address).call() >= amount:
                return
            tx = from_contract.functions.approve(self.address, amount).build_transaction({
                'from': account.address,
                'nonce': self.w3.eth.get_transaction_count(account.address),
                'gas': 500000,
                'maxFeePerGas': 200000000,
                'maxPriorityFeePerGas': 100000000,
            })
            self._send_tx_and_wait(account, tx)

        @modules.handlers.exception_handler
        def _swap():
            steps = self._get_steps(asset_from, asset_to, amount)
            tx = self.contract.functions.multiSwap(steps, amount, 1000).build_transaction({
                "from": account.address,
                "nonce": self.w3.eth.get_transaction_count(account.address),
                'gas': 500000,
                'maxFeePerGas': 200000000,
                'maxPriorityFeePerGas': 100000000,
            })
            self._send_tx_and_wait(account, tx)
        
        _approve()
        _swap()
    
    def add_liquidity(self):
        ...

    def _get_steps(self, asset_from: str, asset_to: str, amount: int):
        address_from = settings.TOKENS[asset_from]["ADDRESS"]
        address_to = settings.TOKENS[asset_to]["ADDRESS"]
        router_api = f"https://bartio-bex-router.berachain-devnet.com/dex/route?fromAsset={address_from}&toAsset={address_to}&amount={amount}"
        resp = requests.get(router_api).json()
        steps = [(
            int(step["poolIdx"]), 
            self.w3.to_checksum_address(step["base"]), 
            self.w3.to_checksum_address(step["quote"]), 
            step["isBuy"]
        ) for step in resp["steps"]]
        
        return steps