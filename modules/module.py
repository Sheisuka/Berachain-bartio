import web3

import modules.utility


class Module:
    def __init__(self, w3: web3.Web3, address: str, abi_path: str) -> None:
        self.w3: web3.Web3 = w3
        self.address: str = address
        self.contract: web3.contract.Contract = modules.utility._get_contract(w3, abi_path, address)
