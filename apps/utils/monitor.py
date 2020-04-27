import os
import sys
import django

sys.path.append(r'E:\PycharmProjects\DRMDEMO')

os.chdir(r'E:\PycharmProjects\DRMDEMO')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DRMDEMO.settings")
django.setup()
from web3 import Web3
from apps.operations import tasks
import json


def loadcontact(w3, contract):
    fn_abi = 'F:\\onedrive\\blockchain\\code\\final\\demo\\{0}.abi'.format(contract)
    fn_addr = 'F:\\onedrive\\blockchain\\code\\final\\demo\\{0}.addr'.format(contract)

    with open(fn_abi) as f:
        abi = json.load(f)

    with open(fn_addr) as f:
        addr = f.read()
        addr = Web3.toChecksumAddress(addr.lower())

    return w3.eth.contract(address=addr, abi=abi)


w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

action = loadcontact(w3, 'cys')

sendAddMsgFilter = action.events.sendAddMsg.createFilter(fromBlock=0)
sendMsgFilter = action.events.sendMsg.createFilter(fromBlock=0)
sendPurchaseMsgFilter = action.events.sendPurchaseMsg.createFilter(fromBlock=0)
senduploadMsgFilter = action.events.senduploadMsg.createFilter(fromBlock=0)
while True:
    try:
        for event in sendPurchaseMsgFilter.get_new_entries():
            if event.args._type == 1:
                tasks.purchaseTask.delay(event.args._form, event.args._id, event.args._productId, event.args._permission,
                                         event.args._timestamp, event.args._money, event.transactionHash.hex(),event.args._projectname)
                # print(event.args)
            if event.args._type == 2:
                tasks.updateTask.delay(event.args._form, event.args._id, event.args._productId, event.args._permission,
                                       event.args._timestamp, event.args._money, event.transactionHash.hex(),event.args._projectname)
        for event in sendMsgFilter.get_new_entries():
            if event.args._type == 1:
                tasks.modifyUpDrmerTask.delay(event.args._msg)
            if event.args._type == 2:
                tasks.modifyDownDrmerTask.delay(event.args._msg)
            if event.args._type == 3:
                tasks.refundTask.delay(event.args._from, event.args._msg)
            if event.args._type == 4:
                tasks.becomeproTask.delay(event.args._from)
            if event.args._type == 5:
                tasks.exitproTask.delay(event.args._from)
            if event.args._type == 7:
                tasks.modifyUpAdminTask.delay(event.args._msg)
            if event.args._type == 8:
                tasks.modifyDownAdminTask.delay(event.args._msg)
        for event in sendAddMsgFilter.get_new_entries():
            tasks.addTask.apply_async(args=(event.args._from, event.args._name, event.args._id, event.args._hashLink, event.args._price,
                                event.transactionHash.hex(), event.args._desc, event.args._status, event.args._demoLink))
        for event in senduploadMsgFilter.get_new_entries():
            tasks.receiveKeyTask.delay(event.args._purchaseId, event.args._ipfshash)
    except Exception as e:
        print(e)
        continue
    finally:
        continue
