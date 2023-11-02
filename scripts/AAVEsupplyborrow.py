# Import the required libraries
import web3
import aave
import os

# import quickswap
WALLET_PUBLIC = os.environ['WALLET_PUBLIC']
WALLET_PRIVATEKEY = os.environ['WALLET_PRIVATEKEY']

# Connect to the Polygon network
provider = web3.Web3.HTTPProvider("https://rpc-mainnet.maticvigil.com")
w3 = web3.Web3(provider)

# Set your account address and private key
account = WALLET_PUBLIC
private_key = WALLET_PRIVATEKEY

# Initialize the Aave lending pool contract
lending_pool = aave.LendingPool(w3, "0x8dFf5E27EA6b7AC08EbFdf9eB090F32ee9a30fcf")

# Get the address of the Matic and USDC tokens on Polygon
matic_token = "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270"
usdc_token = "0x2791bca1f2de4661ed88a30c99a7a9449aa84174"

# Get the address of the corresponding aTokens and debtTokens
a_matic_token = lending_pool.get_atoken_address(matic_token)
a_usdc_token = lending_pool.get_atoken_address(usdc_token)
variable_debt_usdc_token = lending_pool.get_variable_debt_token_address(usdc_token)

# Get the amount of Matic supplied by the account
matic_balance = w3.eth.get_balance(account)

# Enable Matic as collateral
# lending_pool.set_user_use_reserve_as_collateral(matic_token, True, account, private_key)

# Get the maximum amount of USDC that can be borrowed
max_borrow_usdc = lending_pool.get_max_borrow_amount_in_token(usdc_token, account)

# Borrow USDC at variable rate
# lending_pool.borrow(usdc_token, max_borrow_usdc, 2, account, private_key)

# Print the results
print(f"You have supplied {matic_balance} Matic as collateral.")
print(f"You have borrowed {max_borrow_usdc} USDC at variable rate.")
