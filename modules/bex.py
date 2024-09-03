import eth_abi
import web3
import web3.contract
import web3.utils

import requests

import settings
import modules
import modules.module
import modules.utility
import modules.handlers


class Bex(modules.module.Module):
    def __init__(self, w3: web3.Web3):
        super().__init__(w3, settings.DAPPS["BEX"]["ADDRESS"], settings.DAPPS["BEX"]["ABI_PATH"])
        self.croc_swap_contract: web3.contract.Contract = modules.utility._get_contract(
            self.w3, settings.DAPPS["CROCSWAP"]["ADDRESS"], settings.DAPPS["CROCSWAP"]["ABI_PATH"],
        )
        self.croc_query_contract: web3.contract.Contract = modules.utility._get_contract(
            self.w3, settings.DAPPS["CROCQUERY"]["ADDRESS"], settings.DAPPS["CROCQUERY"]["ABI_PATH"],
        )

    def swap(self, account: web3.Account, base: str, quote: str, amount: int):
        self._approve(account, base, amount)
        self._swap(account, base, quote, amount)
    
    def add_liquidity(self, account: web3.Account, base: str, quote: str, lpAddress) -> None:
        ...

    def _add_liquidity(self, account: web3.Account, base: str, quote: str, amount: int) -> None:
        def _get_cmd() -> bytes:
            price = ...
            code: int = 31
            pool_id: int = 36000 # the index of the pool
            bid_tick: int = 0 # 0 for full-range liquidity
            ask_tick: int = 0 # 0 for full-range liquidity
            limit_lower: int = 0 # the minimum acceptable curve price.
            limit_higher: int = 0 # the maximum acceptable curve price.
            reserve_flags: int = 0
            lpConduit: str = "" # the address of LP token
            cmd: bytes = eth_abi.encode(["uint8", "address", "address", "uint256", "int24", "int24", "uint128", "uint128", "uint128", "uint8", "address"],
                                [code, base, quote, pool_id, bid_tick, ask_tick, amount, limit_lower, limit_higher, reserve_flags, ])
            return cmd
    
        cmd: bytes = _get_cmd()
        callpath: int = 128
        tx = self.croc_swap_contract.functions.userCmd(callpath, cmd).build_transaction({
            "from": account.address,
            "nonce": self.w3.eth.get_transaction_count(account.address),
            "gas": 500000,
            "maxFeePerGas": 200000000,
            "maxPriorityFeePerGas": 100000000,
        })
        self._send_tx_and_wait(account, tx)


    def _get_steps(self, base: str, quote: str, amount: int):
        router_api = f"https://bartio-bex-router.berachain-devnet.com/dex/route?fromAsset={base}&toAsset={quote}&amount={amount}"
        resp = requests.get(router_api).json()
        print(resp)
        steps = [
            (
                int(step["poolIdx"]), 
                self.w3.to_checksum_address(step["base"]), 
                self.w3.to_checksum_address(step["quote"]), 
                step["isBuy"]
            ) for step in resp["steps"]
        ]
        
        return steps

    def _swap(self, account: web3.Account, base: str, quote: str, amount: int):
        steps = self._get_steps(base, quote, amount)
        tx = self.contract.functions.multiSwap(steps, amount, 1).build_transaction({
            "from": account.address,
            "nonce": self.w3.eth.get_transaction_count(account.address),
            'gas': 500000,
            'maxFeePerGas': 200000000,
            'maxPriorityFeePerGas': 100000000,
        })
        self._send_tx_and_wait(account, tx)