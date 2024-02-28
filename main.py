from eth_account import Account
from loguru import logger
from bera_tools import BeraChainTools
from config.address_config import (
    usdc_address, wbear_address, weth_address, bex_approve_liquidity_address,
    usdc_pool_liquidity_address, weth_pool_liquidity_address
)
import os
from config.address_config import honey_swap_address, usdc_address, honey_address

    
from config.address_config import bend_address, weth_address, honey_address, bend_pool_address

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import ooga_booga_address, honey_address

from eth_account import Account
from loguru import logger
from solcx import install_solc

from bera_tools import BeraChainTools
from config.address_config import ooga_booga_address, honey_address

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools

def LingShui(key):


    address = ""
    wallet_key = ""

    file_path = './wallet.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.readlines()
        print(content)
        address = content[0].replace("\n", "").split(':')[-1]
        wallet_key = content[1].replace("\n", "").split(':')[-1]
    else:
        account = Account.create()
        wallet_key = account.key.hex()
        address = account.address
        WriteKey(f'address:{address}\nkey:{wallet_key}')


    logger.debug(f'address:{address}')
    logger.debug(f'key:{wallet_key}')

    # TODO 填写你的 YesCaptcha client key 或者2Captcha API Key 或者 ez-captcha ClientKey
    
    client_key = f'{key}'
    # 使用yescaptcha solver googlev3
    bera = BeraChainTools(private_key=wallet_key, client_key=client_key,solver_provider='yescaptcha',rpc_url='https://rpc.ankr.com/berachain_testnet')
    # 使用2captcha solver googlev3
    # bera = BeraChainTools(private_key=wallet_key, client_key=client_key,solver_provider='2captcha',rpc_url='https://rpc.ankr.com/berachain_testnet')
    # 使用ez-captcha solver googlev3
    # bera = BeraChainTools(private_key=wallet_key, client_key=client_key,solver_provider='ez-captcha',rpc_url='https://rpc.ankr.com/berachain_testnet')

    # 不使用代理
    result = bera.claim_bera()
    # 使用代理
    # result = bera.claim_bera(proxies={'http':"http://127.0.0.1:8888","https":"http://127.0.0.1:8888"})
    logger.debug(result.text)
    return wallet_key

def Bex(wallet_key):
    account = Account.from_key(wallet_key)
    bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

    # bex 使用bera交换usdc
    bera_balance = bera.w3.eth.get_balance(account.address)
    result = bera.bex_swap(int(bera_balance * 0.2), wbear_address, usdc_address)
    logger.debug(result)
    # bex 使用usdc交换weth
    usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
    result = bera.bex_swap(int(usdc_balance * 0.2), usdc_address, weth_address)
    logger.debug(result)

    # 授权usdc
    approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), usdc_address)
    logger.debug(approve_result)
    # bex 增加 usdc 流动性
    usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
    result = bera.bex_add_liquidity(int(usdc_balance * 0.5), usdc_pool_liquidity_address, usdc_address)
    logger.debug(result)

    # 授权weth
    approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), weth_address)
    logger.debug(approve_result)
    # bex 增加 weth 流动性
    weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
    result = bera.bex_add_liquidity(int(weth_balance * 0.5), weth_pool_liquidity_address, weth_address)
    logger.debug(result)

def Honey(wallet_key):
    account = Account.from_key(wallet_key)
    bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

    # 授权usdc
    approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), usdc_address)
    logger.debug(approve_result)
    # 使用usdc mint honey
    usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
    result = bera.honey_mint(int(usdc_balance * 0.5))
    logger.debug(result)

    # 授权honey
    approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), honey_address)
    logger.debug(approve_result)
    # 赎回 
    honey_balance = bera.honey_contract.functions.balanceOf(account.address).call()
    result = bera.honey_redeem(int(honey_balance * 0.5))
    logger.debug(result)



def Bend(wallet_key):

    account = Account.from_key(wallet_key)
    bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

    # 授权
    approve_result = bera.approve_token(bend_address, int("0x" + "f" * 64, 16), weth_address)
    logger.debug(approve_result)
    # deposit
    weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
    result = bera.bend_deposit(int(weth_balance), weth_address)
    logger.debug(result)

    # borrow
    balance = bera.bend_contract.functions.getUserAccountData(account.address).call()[2]
    logger.debug(balance)
    result = bera.bend_borrow(int(balance * 0.8 * 1e10), honey_address)
    logger.debug(result)

    # 授权
    approve_result = bera.approve_token(bend_address, int("0x" + "f" * 64, 16), honey_address)
    logger.debug(approve_result)
    # 查询数量 
    call_result = bera.bend_borrows_contract.functions.getUserReservesData(bend_pool_address, bera.account.address).call()
    repay_amount = call_result[0][0][4]
    logger.debug(repay_amount)
    # repay
    result = bera.bend_repay(int(repay_amount * 0.9), honey_address)
    logger.debug(result)


def honeyjar(wallet_key):

    account = Account.from_key(wallet_key)
    bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')


    # https://faucet.0xhoneyjar.xyz/mint
    # 授权
    approve_result = bera.approve_token(ooga_booga_address, int("0x" + "f" * 64, 16), honey_address)
    logger.debug(approve_result)
    # 花费4.2 honey mint
    result = bera.honey_jar_mint()
    logger.debug(result)

def contract(wallet_key):
    account = Account.from_key(wallet_key)
    bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

    # 安装0.4.18 版本编译器
    install_solc('0.4.18')
    # 读取sol文件
    with open('config/WETH.sol', 'r') as f:
        code = f.read()
        # 部署合约
        result = bera.deploy_contract(code, '0.4.18')
        logger.debug(result)

def domain(wallet_key):
    account = Account.from_key(wallet_key)
    bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')
    result = bera.create_bera_name()
    logger.debug(result)


def ReadKey():
    # Define the path to the file
    file_path = './client_key.txt'

    # Open the file in read mode ('r') and read the contents
    with open(file_path, 'r') as file:
        content = file.read()
        return content

def WriteKey(text = ''):
    # Define the path to the file
    file_path = './wallet.txt'

    # Open the file in write mode ('w') and write the text
    with open(file_path, 'w') as file:
        file.write(text)

    print("Wallet written to file successfully.")


if __name__ == '__main__':
    # print(get_no_captcha_google_token(''))
    client_key = ReadKey()
    wallet_key = LingShui(client_key)
    Bex(wallet_key)
    Honey(wallet_key)
    Bend(wallet_key)
    honeyjar(wallet_key)
    contract(wallet_key)
    domain(wallet_key)
