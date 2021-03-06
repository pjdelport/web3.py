import pytest

from web3.utils.encoding import force_bytes


@pytest.fixture(autouse=True)
def wait_for_first_block(web3, wait_for_block):
    wait_for_block(web3)


def test_eth_getCode(web3, wait_for_transaction, MATH_CODE, MATH_RUNTIME):
    txn_hash = web3.eth.sendTransaction({
        "from": web3.eth.coinbase,
        "data": MATH_CODE,
        "gas": 3000000,
    })

    wait_for_transaction(txn_hash)

    txn_receipt = web3.eth.getTransactionReceipt(txn_hash)
    contract_address = txn_receipt['contractAddress']

    assert force_bytes(web3.eth.getCode(contract_address)) == MATH_RUNTIME
