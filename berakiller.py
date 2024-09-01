import web3
import web3.contract

import pathlib
import typing
import random
import web3.exceptions

import settings
import modules.bex
import modules.honey_swap
import modules.utility


class Berakiller:
    def __init__(self) -> None:
        self.accounts: typing.List[web3.Account] = self._get_accounts()
        self.w3: web3.Web3 = self._get_w3()
        self.honey_swap: modules.honey_swap.HoneySwap = modules.honey_swap.HoneySwap(self.w3)
        self.bex: modules.bex.Bex = modules.bex.Bex(self.w3)
    
    def test(self) -> None:
        self.swap_on_bex()
    
    def mint_honey(self) -> None:
        """Mint honey for usdc"""
        account: web3.Account = self.accounts[0]
        usdc: web3.contract.Contract = modules.utility._get_contract(self.w3, settings.USDC_ABI_PATH, settings.USDC_ADDRESS)
        usdc_balance: int = usdc.functions.balanceOf(account.address).call()
        if usdc_balance != 0:
            amount = random.randint(1 + usdc_balance // 8, usdc_balance // 4) # from 12.5% to 25% of the balance
            self.honey_swap.mint(account, usdc.address, amount)
            print("Honey minted")
        else:
            print(f"Zero usdc on {account.address}")
    
    def redeem_honey(self) -> None:
        """Redeem usdc for honey"""
        account: web3.Account = self.accounts[0]
        honey: web3.contract.Contract = modules.utility._get_contract(self.w3, settings.HONEY_ABI_PATH, settings.HONEY_ADDRESS)
        honey_balance: int = honey.functions.balanceOf(account.address).call()
        if honey_balance != 0:
            amount = random.randint(1 + honey_balance // 8, honey_balance // 4) # from 12.5% to 25% of the balance
            self.honey_swap.reedem(account, settings.USDC_ADDRESS, amount)
            print("USDC redeemed")
        else:
            print(f"Zero honey on {account.address}")
    
    def swap_on_bex(self) -> None:
        """Swap assets on BEX"""
        account: web3.Account = self.accounts[0]
        self.bex.swap(account, "WBERA", "USDC")

    def _get_w3(self) -> web3.Web3:
        """Get web3 instance"""
        w3 =  web3.Web3(web3.HTTPProvider(settings.RPC_URL))
        return w3


    def _get_accounts(self) -> typing.List[web3.Account]:
        """Get shuffled accounts from file with private keys"""
        path = pathlib.Path(settings.WALLETS_PATH)
        if not path.exists():
            raise FileNotFoundError(f"No private keys were found at {path.absolute()}")
        with path.open() as keys_file:
            accounts = list()
            for line_i, key in enumerate(keys_file):
                try:
                    account = web3.Account.from_key(key.strip())
                    accounts.append(account)
                except Exception as error:
                    print(f"Invalid private key at line {line_i}.")
            if not accounts:
                print("No valid private keys. Exit.")
                exit()
            random.shuffle(accounts)
            return accounts
        
    def _bera_is_low(self, address: str) -> bool:
        """Check if bera balance is low"""
        return self.w3.eth.get_balance(address) * settings.BERA_DECIMALS > settings.LOW_BERA_AMOUNT
