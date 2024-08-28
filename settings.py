# Если True, то запросить $BERA в случае низкого баланса, иначе скип кошелек  
DRIP_IF_NOT_SUFFICIENT = True

# Баланс меньше LOW_BERA_AMOUNT считается низким
LOW_BERA_AMOUNT = 0.1

BERA_DECIMALS = 18

USDC_ADDRESS = "0xd6D83aF58a19Cd14eF3CF6fe848C9A4d21e5727c"

USDC_ABI_PATH = "abis/core/USDC.json"

HONEY_ADDRESS = "0x0E4aaF1351de4c0264C5c7056Ef3777b41BD8e03"

HONEY_ABI_PATH = "abis/core/HONEY.json"

USDC_DECIMALS = 6

SHUFFLE_WALLETS = True

TIME_DELAY_ROUTES = [30, 50]

HONEYSWAP_ADDRESS = "0xAd1782b2a7020631249031618fB1Bd09CD926b31"

HONEYSWAP_ABI_PATH = "abis/core/HoneyFactory.json"

RPC_URL = "https://bartio.drpc.org"

WALLETS_PATH = "private_keys.txt"

RETRIES_COUNT = 2