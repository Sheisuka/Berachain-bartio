import web3

import typing
import json
import pathlib


def _load_abi(abi_path: str) -> typing.Any:
    """Load ABI via abi_path"""
    path = pathlib.Path(abi_path)
    if not path.exists():
        raise FileNotFoundError(f"No ABI was found at {abi_path}")
    with path.open() as abi_file:
        return json.load(abi_file)
    
def _get_contract(w3: web3.Web3, address: str, abi_path: str) -> web3.contract.Contract:
    """Create contract with address and ABI"""
    abi = _load_abi(abi_path)
    return w3.eth.contract(address=address, abi=abi)