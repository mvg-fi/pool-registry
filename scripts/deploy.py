from brownie import ZERO_ADDRESS, AddressProvider, PoolInfo, Registry, Swaps, accounts, BasePoolRegistry, CryptoRegistry
from brownie.network.gas.strategies import GasNowScalingStrategy

from scripts.add_pools import main as add_pools

# modify this prior to mainnet use
deployer = accounts.load('owner')

WETH_ADDRESS = "0xBac65f64cd7Ac8a2e71800C504b1E61D8c405015"
ADDRESS_PROVIDER = "0xc0ba8A26be45EfCBD4252C317f0b1b02776022C0"
GAUGE_CONTROLLER = deployer.address

gas_strategy = 50000007
print('gas_strategy: ',gas_strategy)


def deploy_registry():
    """
    Deploy `Registry`, add all current pools, and set the address in `AddressProvider`.
    """
    balance = deployer.balance()

    provider = AddressProvider.at(ADDRESS_PROVIDER)
    registry = Registry.deploy(
        ADDRESS_PROVIDER, GAUGE_CONTROLLER, {"from": deployer, "gas_price": gas_strategy}
    )
    add_pools(registry, deployer)
    provider.set_address(0, registry, {"from": deployer, "gas_price": gas_strategy})

    print(f"Registry deployed to: {registry.address}")
    print(f"Total gas used: {(balance - deployer.balance()) / 1e18:.4f} eth")


def deploy_pool_info():
    """
    Deploy `PoolInfo` and set the address in `AddressProvider`.
    """
    balance = deployer.balance()

    provider = AddressProvider.at(ADDRESS_PROVIDER)

    pool_info = PoolInfo.deploy(provider, {"from": deployer, "gas_price": gas_strategy})

    if provider.max_id() == 0:
        provider.add_new_id(
            pool_info, "PoolInfo Getters", {"from": deployer, "gas_price": gas_strategy}
        )
    else:
        provider.set_address(1, pool_info, {"from": deployer, "gas_price": gas_strategy})

    print(f"PoolInfo deployed to: {pool_info.address}")
    print(f"Total gas used: {(balance - deployer.balance()) / 1e18:.4f} eth")


def deploy_swaps():
    """
    Deploy `Swaps` and set the address in `AddressProvider`.
    """
    balance = deployer.balance()

    provider = AddressProvider.at(ADDRESS_PROVIDER)

    swaps = Swaps.deploy(provider, ZERO_ADDRESS, WETH_ADDRESS, {"from": deployer, "gas_price": gas_strategy})

    if provider.max_id() == 1:
        provider.add_new_id(swaps, "Exchanges", {"from": deployer, "gas_price": gas_strategy})
    else:
        provider.set_address(2, swaps, {"from": deployer, "gas_price": gas_strategy})

    print(f"PoolInfo deployed to: {swaps.address}")
    print(f"Total gas used: {(balance - deployer.balance()) / 1e18:.4f} eth")

def deploy_base_pool_registry_and_crypto_registry():
    """
    Deploy `CryptoRegistry`,`BasePoolRegistry` and set the address in `AddressProvider`.
    """
    balance = deployer.balance()

    provider = AddressProvider.at(ADDRESS_PROVIDER)

    bpRegistry = BasePoolRegistry.deploy({"from": deployer, "gas_price": gas_strategy})
    cRegistry = CryptoRegistry.deploy(ADDRESS_PROVIDER, bpRegistry.address,{"from": deployer, "gas_price": gas_strategy})

    print(f"CryptoRegistry deployed to: {cRegistry.address}")
    print(f"BasePoolRegistry deployed to: {bpRegistry.address}")
    print(f"Total gas used: {(balance - deployer.balance()) / 1e18:.4f} eth")

def main():
    deploy_swaps()