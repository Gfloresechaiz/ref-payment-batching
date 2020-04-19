#!/usr/bin/env python3

from bitcoin import rpc
from bitcoin.core import x, lx, b2x, b2lx
from bitcoin.core import CScript
import csv
from datetime import datetime

with open('data4.csv', mode='w') as data:
  data_writer = csv.writer(data, delimiter=',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
  ## Arbitrary block height; might differ from average block.
  ## Note: python-bitcoin 0.8 doesn't work for me on segwit blocks, so I
  ## chose a block from a few weeks ago.
  height = 150000

  while height <= 625024:
    ## Setup
    proxy = rpc.Proxy()
    seen_txids = {}
    unbatched_block_total = 0
    batched_block_total = 0

    ## Get the block
    block = proxy.getblock(proxy.getblockhash(height))

    # ## For each transaction in the block
    # for tx in block.vtx:
    #   ## Skip coinbase transactions sice they can't be spent in the same
    #   ## block (100 block maturation rule)
    #   if tx.is_coinbase():
    #     continue

    #   ## Add the transaction's txid to a dict
    #   seen_txids[b2lx(tx.GetTxid())] = True

    #   ## Calculate the transaction's byte size.
    #   transaction_size = len(tx.serialize())

    #   ## Add the transaction size to our base total
    #   unbatched_block_total += transaction_size
      
    #   ## For each input in the transaction, see if its prevout (previous
    #   ## output) matches the txid of any other earlier transaction in this
    #   ## block.
    #   match = False
    #   for tx_input in tx.vin:
    #     prevout = b2lx(tx_input.prevout.hash)
    #     ## If it does match, we add only the total size of the outputs to
    #     ## our hypothetical fully-batched block
    #     if prevout in seen_txids:
    #       output_size = 0
    #       for tx_output in tx.vout:
    #         output_size += len(tx_output.serialize())
    #       batched_block_total += output_size
    #       match = True
    #       break

    #   ## If it doesn't match, we add the full transaction size to our
    #   ## hypothetical fully-batched block
    #   if match == False:
    #     batched_block_total += transaction_size
    
    # savedBytes = unbatched_block_total - batched_block_total
    # savedPercentage = 0
    # if unbatched_block_total > 0:
    #   savedPercentage = savedBytes / unbatched_block_total
    # ## Print some statistics
    time = datetime.utcfromtimestamp(block.nTime)
    formattedTime = time.strftime("%d/%m/%Y")
    data_writer.writerow([height, formattedTime])

    height += 1

