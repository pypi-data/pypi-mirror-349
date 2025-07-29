import asyncio
from web3 import Web3
from uuid import UUID
from celium_collateral_contracts.common import (
    get_web3_connection,
    get_account,
    validate_address_format,
    get_miner_collateral,
)
from celium_collateral_contracts.deposit_collateral import deposit_collateral
from celium_collateral_contracts.reclaim_collateral import reclaim_collateral
from celium_collateral_contracts.finalize_reclaim import finalize_reclaim
from celium_collateral_contracts.deny_request import deny_reclaim_request
from celium_collateral_contracts.slash_collateral import slash_collateral
from celium_collateral_contracts.get_collaterals import get_deposit_events
from celium_collateral_contracts.get_reclaim_requests import get_reclaim_process_started_events
from celium_collateral_contracts.get_eligible_executors import get_eligible_executors
from celium_collateral_contracts.update_validator_for_miner import update_validator_for_miner
from celium_collateral_contracts.get_validator_of_miner import get_validator_of_miner

class CollateralContract:
    def __init__(self, network: str, contract_address: str, validator_keystr=None, miner_keystr=None):
        self.network = network
        self.contract_address = contract_address
        self.validator_keystr = validator_keystr
        self.miner_keystr = miner_keystr
        self.w3 = None
        self.validator_account = None
        self.validator_address = None
        self.miner_account = None
        self.miner_address = None

    async def initialize(self):
        """Asynchronous initialization logic."""
        self.w3 = await get_web3_connection(self.network)
        try:
            self.validator_account = await get_account(self.validator_keystr) if self.validator_keystr else None
            self.validator_address = self.validator_account.address if self.validator_account else None
        except Exception as e:
            print(f"Warning: Failed to initialize validator account. Error: {e}")

        try:
            self.miner_account = await get_account(self.miner_keystr) if self.miner_keystr else None
            self.miner_address = self.miner_account.address if self.miner_account else None
        except Exception as e:
            print(f"Warning: Failed to initialize miner account. Error: {e}")

        self.contract_address = contract_address

    async def deposit_collateral(self, amount_tao, executor_uuid):
        """Deposit collateral into the contract."""
        return await deposit_collateral(
            self.w3,
            self.miner_account,
            amount_tao,
            self.contract_address,
            self.validator_address,
            executor_uuid,
        )

    async def reclaim_collateral(self, amount_tao, url, executor_uuid):
        """Initiate reclaiming collateral."""
        return await reclaim_collateral(
            self.w3,
            self.miner_account,
            amount_tao,
            self.contract_address,
            url,
            executor_uuid,
        )

    async def finalize_reclaim(self, reclaim_request_id):
        """Finalize a reclaim request."""
        return await finalize_reclaim(
            self.w3,
            self.validator_account,
            reclaim_request_id,
            self.contract_address,
        )

    async def deny_reclaim_request(self, reclaim_request_id, url):
        """Deny a reclaim request."""
        return await deny_reclaim_request(
            self.w3,
            self.validator_account,
            reclaim_request_id,
            url,
            self.contract_address,
        )

    async def slash_collateral(self, amount_tao, url, executor_uuid):
        """Slash collateral from a miner."""
        return await slash_collateral(
            self.w3,
            self.validator_account,
            self.miner_address,
            amount_tao,
            self.contract_address,
            url,
            executor_uuid,
        )

    async def get_miner_collateral(self):
        """Get the collateral amount for a miner."""
        return await get_miner_collateral(self.w3, self.contract_address, self.miner_address)

    async def get_deposit_events(self, block_start, block_end):
        """Fetch deposit events within a block range."""
        return await get_deposit_events(
            self.w3,
            self.contract_address,
            block_start,
            block_end,
        )

    async def get_eligible_executors(self, executor_uuids):
        """Get the list of eligible executors for a miner."""
        return await get_eligible_executors(
            self.w3,
            self.contract_address,
            self.miner_address,
            executor_uuids,
        )

    async def get_balance(self, address):
        """Get the balance of an Ethereum address."""
        validate_address_format(address)
        balance = await self.w3.eth.get_balance(address)
        return self.w3.from_wei(balance, "ether")

    async def get_reclaim_requests(self):
        """Fetch claim requests from the latest 100 blocks."""
        latest_block = await self.w3.eth.block_number
        return await get_reclaim_process_started_events(
            self.w3, self.contract_address, latest_block - 100, latest_block
        )

    async def update_validator_for_miner(self, new_validator):
        return await update_validator_for_miner(
            self.w3,
            self.miner_account,
            self.contract_address,
            self.miner_address,
            new_validator,
        )

    async def get_validator_of_miner(self):
        """Retrieve the validator associated with the miner."""
        return await get_validator_of_miner(self.w3, self.contract_address, self.miner_address)
         

async def main():
    import os
    import time

    # Configuration
    network = "test"
    contract_address = "0x8911acCB78363B3AD6D955892Ba966eb6869A2e6"
    validator_key = "434469242ece0d04889fdfa54470c3685ac226fb3756f5eaf5ddb6991e1698a3"
    miner_key = "259e0eded00353f71eb6be89d8749ad12bf693cbd8aeb6b80cd3a343c0dc8faf"

    # Initialize CollateralContract instance
    contract = CollateralContract(network, contract_address, validator_key, miner_key)
    await contract.initialize()

    # Verify chain ID
    chain_id = await contract.w3.eth.chain_id
    print(f"Verified chain ID: {chain_id}")

    # Check balances
    validator_balance = await contract.get_balance(contract.validator_address)
    miner_balance = await contract.get_balance(contract.miner_address)
    print("Validator Balance:", validator_balance)
    print("Miner Balance:", miner_balance)

    # Deposit collateral (optional: uncomment to use)
    deposit_tasks = [
        ("3a5ce92a-a066-45f7-b07d-58b3b7986464", 0.0005),
        ("72a1d228-3c8c-45cb-8b84-980071592589", 0.0005),
        ("15c2ff27-0a4d-4987-bbc9-fa009ef9f7d2", 0.0005),
        ("335453ad-246c-4ad5-809e-e2013ca6c07e", 0.0005),
        ("89c66519-244f-4db0-b4a7-756014d6fd24", 0.0005),
        ("af3f1b82-ff98-44c8-b130-d948a2a56b44", 0.0005),
        ("ee3002d9-71f8-4a83-881d-48bd21b6bdd1", 0.0005),
        ("4f42de60-3a41-4d76-9a19-d6d2644eb57f", 0.0005),
        ("7ac4184e-e84f-40cb-b6a0-9cf79a1a573c", 0.0005),
        ("9d14f803-dc8c-405f-99b5-80f12207d4e5", 0.0005),
        ("2a61e295-fd0f-4568-b01c-1c38c21573ac", 0.0005),
        ("e7fd0b3f-4a42-4a5d-bda6-8e2f4b5cb92a", 0.0005),
        ("f2c2a71d-5c44-4ab9-a87e-0ac1f278b6d6", 0.0005),
        ("1ec29b47-3d6b-4cc3-b71d-6c97fcbf1e89", 0.0005),
    ]

    # Example deposit (uncomment to perform deposits)
    # for uuid_str, amount in deposit_tasks:
    #     print(f"Depositing collateral for executor {uuid_str}...")
    #     await contract.deposit_collateral(amount, uuid_str)

    # Verify collateral
    collateral = await contract.get_miner_collateral()
    collateral_in_tao = contract.w3.from_wei(collateral, "ether")
    print("[COLLATERAL]:", collateral_in_tao)

    # List eligible executors
    executor_uuids = [uuid for uuid, _ in deposit_tasks]
    eligible_executors = await contract.get_eligible_executors(executor_uuids)
    print("Eligible Executors:", eligible_executors)

    # Reclaim collateral example (uncomment to use)
    # reclaim_uuid = "72a1d228-3c8c-45cb-8b84-980071592589"
    # print("Reclaiming collateral...")
    # reclaim_result = await contract.reclaim_collateral(0.00001, "please gimme money back", reclaim_uuid)
    # print("Reclaim Result:", reclaim_result)

    # Final collateral check
    final_collateral = await contract.get_miner_collateral()
    final_collateral_in_tao = contract.w3.from_wei(final_collateral, "ether")
    print("[FINAL COLLATERAL]:", final_collateral_in_tao)

    # Check final balances
    validator_balance = await contract.get_balance(contract.validator_address)
    miner_balance = await contract.get_balance(contract.miner_address)
    print("Validator Balance:", validator_balance)
    print("Miner Balance:", miner_balance)

    # Validator lookup
    try:
        validator = await contract.get_validator_of_miner()
        print(f"Validator for miner {contract.miner_address}: {validator}")
    except Exception as e:
        print(f"Error retrieving validator for miner: {e}")

    # Update validator
    new_validator = "0x94C54725D6c8500aFf59716F33EdE6AA1FaD86CF"
    print(f"Updating validator for miner to {new_validator}...")
    try:
        update_result = await contract.update_validator_for_miner(new_validator)
        print("Update Validator Result:", update_result)
    except Exception as e:
        print(f"Error updating validator for miner: {e}")

    # Confirm updated validator
    try:
        validator = await contract.get_validator_of_miner()
        print(f"Validator for miner {contract.miner_address}: {validator}")
    except Exception as e:
        print(f"Error retrieving validator for miner: {e}")

    print("✅ Contract lifecycle completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
