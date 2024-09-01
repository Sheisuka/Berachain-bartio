# Если True, то запросить $BERA в случае низкого баланса, иначе скип кошелек  
DRIP_IF_NOT_SUFFICIENT = True

# Баланс меньше LOW_BERA_AMOUNT считается низким
LOW_BERA_AMOUNT = 0.1

BERA_DECIMALS = 18

SHUFFLE_WALLETS = True

TIME_DELAY_ROUTES = [30, 50]


RPC_URL = "https://bartio.drpc.org"

WALLETS_PATH = "private_keys.txt"

RETRIES_COUNT = 2


TOKENS = {
    "USDC": {
        "ADDRESS": "0xd6D83aF58a19Cd14eF3CF6fe848C9A4d21e5727c",
        "ABI_PATH": "abis/core/USDC.json",
        "DECIMALS": 6
    },
    "HONEY": {
        "ADDRESS": "0x0E4aaF1351de4c0264C5c7056Ef3777b41BD8e03",
        "ABI_PATH": "abis/core/HONEY.json",
        "DECIMALS": 18,
    },
    "WBERA": {
        "ADDRESS": "0x7507c1dc16935B82698e4C63f2746A2fCf994dF8",
        "ABI_PATH": "abis/core/WBERA.json",
        "DECIMALS": 18,
    },
}

DAPPS = {
    "BEX": {
        "ADDRESS": "0x21e2C0AFd058A89FCf7caf3aEA3cB84Ae977B73D",
        "ABI_PATH": "abis/bex/BeraCrocMultiSwap.json",
    },
    "HONEYSWAP": {
        "ADDRESS": "0xAd1782b2a7020631249031618fB1Bd09CD926b31",
        "ABI_PATH": "abis/core/HoneyFactory.json"
    },
}