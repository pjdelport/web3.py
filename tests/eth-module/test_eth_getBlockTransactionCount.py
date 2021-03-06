import collections
import itertools
import pytest

from web3.web3.rpcprovider import TestRPCProvider


@pytest.fixture(autouse=True)
def wait_for_first_block(web3, wait_for_block):
    wait_for_block(web3)


def test_eth_getBlockTransactionCount(web3, extra_accounts, wait_for_transaction):
    if isinstance(web3.currentProvider, TestRPCProvider):
        pytest.skip("testrpc doesn't implement `getBlockTransactionCount`")

    transaction_hashes = []

    # send some transaction
    for _ in range(5):
        transaction_hashes.append(web3.eth.sendTransaction({
            "from": web3.eth.coinbase,
            "to": extra_accounts[1],
            "value": 1,
        }))

    # wait for them to resolve
    for txn_hash in transaction_hashes:
        wait_for_transaction(txn_hash)

    # gather all receipts and sort/group them by block number.
    all_receipts = sorted(
        [web3.eth.getTransactionReceipt(txn_hash) for txn_hash in transaction_hashes],
        key=lambda r: r['blockNumber'],
    )
    all_receipts_by_block = {
        key: tuple(value)
        for key, value in itertools.groupby(all_receipts, lambda r: r['blockNumber'])
    }

    for block_number, block_receipts in all_receipts_by_block.items():
        block = web3.eth.getBlock(block_number)
        block_hash = block['hash']

        assert web3.eth.getBlockTransactionCount(block_number) == len(block_receipts)
        assert web3.eth.getBlockTransactionCount(block_hash) == len(block_receipts)
