import json
from django.test import TestCase

# Create your tests here.
from web3 import Web3


# print(w3.eth.getTransaction('0xc39d2342b3da87d9f4ca8b9cc5104a8a08f33c5097586c7bcd34782b2bb182bb'))
# print(w3.eth.getBlock(26)['timestamp'])


# def loadcontact(w3, contract):
#     fn_abi = 'F:\\onedrive\\blockchain\\code\\final\\demo\\{0}.abi'.format(contract)
#     fn_addr = 'F:\\onedrive\\blockchain\\code\\final\\demo\\{0}.addr'.format(contract)
#
#     with open(fn_abi) as f:
#         abi = json.load(f)
#
#     with open(fn_addr) as f:
#         addr = f.read()
#         addr = Web3.toChecksumAddress(addr.lower())
#
#     return w3.eth.contract(address=addr, abi=abi)


# action = loadcontact(w3, 'cys')
# filter = action.events.sendPurchaseMsg.createFilter(fromBlock=int(26), argument_filters={
#     "_from": '0xA452E25C2FBeebb4E66A031718a227B45ae020b5'})
# oldlist = filter.get_all_entries()
# for event in oldlist:
#     if event.transactionHash.hex() == '0xc39d2342b3da87d9f4ca8b9cc5104a8a08f33c5097586c7bcd34782b2bb182bb':
#         _purchaseId = event.args._purchaseId
#         msg = event.args._msg
#         print(event)
#         if msg == 502:
#             break

# w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
# action = loadcontact(w3, 'cys')
# print(int(Web3.fromWei(100000000000000000000, 'ether')))

# result = action.functions.isProducer('0x7e36b9fc43648c2a1d12a307D759a2F063bcc08f').call()
# print(result ==True)
# print(w3.eth.getTransactionCount(keyring.get_password("DRMDEMO", 'address'))))
# print(w3.eth.getTransaction('0xd3bf1ed527b448f93e0cdb7e7f251de968fa37a4efe08435b6caadf2f9ca02ea'))
# print(w3.eth.getBlock(1)['timestamp'])
# ipfs_hash = action.functions.getLicenseBypurchaseId(int(30)).call({'from':Web3.toChecksumAddress('0xa452e25c2fbeebb4e66a031718a227b45ae020b5')})
# print(ipfs_hash)



