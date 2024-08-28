import web3

import settings
import modules.module
import modules.utility
import modules.handlers


class HoneySwap(modules.module.Module):
    def __init__(self, w3: web3.Web3):
        super().__init__(w3, settings.HONEYSWAP_ADDRESS, settings.HONEYSWAP_ABI_PATH)

    def mint(self, account: web3.Account, asset: str, amount: int) -> None:
        @modules.handlers.error_handler
        def _approve():
            usdc_contract = modules.utility._get_contract(self.w3, settings.USDC_ABI_PATH, settings.USDC_ADDRESS)
            tx = usdc_contract.functions.approve(self.address, amount).build_transaction({
                'gas': 500000,
                'nonce': self.w3.eth.get_transaction_count(account.address),
                'maxFeePerGas': 200000000,
                'maxPriorityFeePerGas': 100000000,
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            self.w3.eth.wait_for_transaction_receipt(tx_hash)

        @modules.handlers.error_handler
        def _mint():
            tx = self.contract.functions.mint(asset, amount, account.address).build_transaction({
                'gas': 500000,
                'nonce': self.w3.eth.get_transaction_count(account.address),
                'maxFeePerGas': 200000000,
                'maxPriorityFeePerGas': 100000000,
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=account.key)
            self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        _approve()
        _mint()


    def reedem(self, account: web3.Account, asset: str, amount: int) -> None:
        @modules.handlers.error_handler
        def _approve():
            honey_contract = modules.utility._get_contract(self.w3, settings.HONEY_ABI_PATH, settings.HONEY_ADDRESS)
            tx = honey_contract.functions.approve(self.address, amount).build_transaction({
                'gas': 500000,
                'nonce': self.w3.eth.get_transaction_count(account.address),
                'maxFeePerGas': 200000000,
                'maxPriorityFeePerGas': 100000000,
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        @modules.handlers.error_handler
        def _mint():
            tx = self.contract.functions.redeem(asset, amount, account.address).build_transaction({
                'gas': 500000,
                'nonce': self.w3.eth.get_transaction_count(account.address),
                'maxFeePerGas': 200000000,
                'maxPriorityFeePerGas': 100000000,
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=account.key)
            self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        _approve()
        _mint()