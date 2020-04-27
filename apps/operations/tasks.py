from __future__ import absolute_import, unicode_literals

import json

import ipfshttpclient
import keyring
import requests
import smtplib
from tempfile import TemporaryFile
from celery import shared_task
from celery_once import QueueOnce
from web3 import Web3
from apps.operations.models import UserMusic, WitchoutUserMusic
from apps.music.models import Music, WithoutMusic
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from apps.users.models import UserProfile, WithoutUserProfile
from DRMDEMO.settings import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from binascii import b2a_hex
from apps.utils.ssl_client import client_ssl

client = client_ssl()
ipfsclient = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')


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


@shared_task(base=QueueOnce, once={'graceful': True, 'timeout': 60 * 10})
def addTask(_from, _name, _id, _hashLink, _price, transactionHash, _desc, _status, _demoLink):
    music = Music.objects.filter(music_hashLink=_hashLink)
    price_list = [str(Web3.fromWei(x, 'ether')) for x in _price]
    if not music:
        music = WithoutMusic()
        music.music_bcId = int(_id)
        music.owneraddress = _from
        music.music_name = _name
        music.music_transactionHash = transactionHash
        music.music_desc = _desc
        music.music_status = 2
        music.music_price1 = price_list[0]
        music.music_price2 = price_list[1]
        music.music_price3 = price_list[2]
        music.music_price4 = price_list[3]
        music.music_price5 = price_list[4]
        music.music_price6 = price_list[5]
        music.music_hashLink = _hashLink
        music.music_demoLink = _demoLink
        music.save()
    else:
        music = music.last()
        music.music_bcId = int(_id)
        music.music_price1 = price_list[0]
        music.music_price2 = price_list[1]
        music.music_price3 = price_list[2]
        music.music_price4 = price_list[3]
        music.music_price5 = price_list[4]
        music.music_price6 = price_list[5]
        music.music_transactionHash = transactionHash
        music.music_status = 2
        music.music_hashLink = _hashLink
        music.music_demoLink = _demoLink
        music.save()
        # 传送密钥服务器
        keyfile = music.keyfile.read()
        send_data = {
            'type': 1,
            'productId': int(_id),
            "status": _status,
            'keyfile': keyfile.decode()
        }
        # print(send_data)
        recvmsg = client.send_msg(send_data)
        if recvmsg == 'ok':
            return 'success'
        else:
            return 'fail'


@shared_task
def modifyUpDrmerTask(id):
    music = Music.objects.filter(music_bcId=int(id))
    if music:
        music = music.first()
        if music.music_status:
            music.music_status = 2
            music.save()
            return 'modify music status fail'
        music.music_status = 2
        music.save()
        send_data = {
            'type': 3,
            'productId': int(id),
            "status": True,
        }
        # print(send_data)
        recvmsg = client.send_msg(send_data)
        if recvmsg == 'ok':
            return 'modify music status success'
        else:
            return 'modify music status fail'

    else:
        withoutmusic = WithoutMusic.objects.filter(music_bcId=int(id)).first()
        if withoutmusic.music_status:
            withoutmusic.music_status = 1
            withoutmusic.save()
            return 'modify music status fail'
        withoutmusic.music_status = 1
        withoutmusic.save()


@shared_task
def modifyDownDrmerTask(id):
    music = Music.objects.filter(music_bcId=int(id))
    if music:
        music = music.first()
        if music.music_status == 0:
            music.music_status = 2
            music.save()
            return 'fail'
        music.music_status = 2
        music.save()
        send_data = {
            'type': 3,
            'productId': int(id),
            "status": False,
        }
        # print(send_data)
        recvmsg = client.send_msg(send_data)
        if recvmsg == 'ok':
            return 'modify music status success'
        else:
            return 'modify music status fail'
    else:
        withoutmusic = WithoutMusic.objects.filter(music_bcId=int(id)).first()
        if withoutmusic.music_status == 0:
            withoutmusic.music_status = 0
            withoutmusic.save()
            return 'fail'
        withoutmusic.music_status = 0
        withoutmusic.save()

@shared_task
def modifyUpAdminTask(id):
    music = Music.objects.filter(music_bcId=int(id))
    if music:
        music = music.first()
        if music.music_status:
            music.music_status = 1
            music.save()
            return 'admin modify music status fail'
        music.music_status = 1
        music.save()
        return "admin modify music status success"

    else:
        withoutmusic = WithoutMusic.objects.filter(music_bcId=int(id)).first()
        if withoutmusic.music_status:
            withoutmusic.music_status = 1
            withoutmusic.save()
            return 'modify music status fail'
        withoutmusic.music_status = 1
        withoutmusic.save()


@shared_task
def modifyDownAdminTask(id):
    music = Music.objects.filter(music_bcId=int(id))
    if music:
        music = music.first()
        if music.music_status == 0:
            music.music_status = 0
            music.save()
            return 'admin modify music status fail'
        music.music_status = 0
        music.save()
        return "admin modify music status success"
    else:
        withoutmusic = WithoutMusic.objects.filter(music_bcId=int(id)).first()
        if withoutmusic.music_status == 0:
            withoutmusic.music_status = 0
            withoutmusic.save()
            return 'fail'
        withoutmusic.music_status = 0
        withoutmusic.save()

@shared_task
def purchaseTask(_form, _id, _productId, _permission, _timestamp, _money, transactionHash, projectname):
    usermusic = UserMusic.objects.filter(music__music_bcId=str(_productId)).filter(
        purchase_permission=int(_permission)).filter(user__address=_form).filter(purchase_status=0)
    if not usermusic:
        withoutusermusic = WitchoutUserMusic()
        withoutusermusic.bought_address = _form
        withoutusermusic.timestamp = _timestamp
        withoutusermusic.purchase_bcId = str(_id)
        withoutusermusic.product_bcId = str(_productId)
        withoutusermusic.purchase_permission = int(_permission)
        withoutusermusic.music_price = str(w3.fromWei(_money, "ether"))
        withoutusermusic.purchase_transactionHash = transactionHash
        withoutusermusic.save()

    if usermusic:
        usermusic = usermusic.last()
        usermusic.purchase_transactionHash = transactionHash
        usermusic.add_time = datetime.now()
        usermusic.purchase_bcId = str(_id)
        usermusic.purchase_permission = int(_permission)
        usermusic.purchase_status = 1
        usermusic.music_price = str(w3.fromWei(_money, "ether"))
        usermusic.timestamp = _timestamp
        usermusic.projectname = projectname.encode().decode("unicode-escape")
        print(projectname.encode().decode("unicode-escape"))
        # print(projectname.encode().decode('unicode-escape').encode('latin1').decode('utf-8'))
        usermusic.save()


@shared_task
def updateTask(_form, _id, _purchaseId, _newPermission, _timestamp, _money, transactionHash, projectname):
    owner = UserProfile.objects.filter(address=_form)
    old_music = UserMusic.objects.filter(purchase_bcId=str(_purchaseId))
    if not owner:
        withoutusermusic = WitchoutUserMusic()
        withoutusermusic.bought_address = _form
        withoutusermusic.timestamp = _timestamp
        withoutusermusic.purchase_bcId = str(_id)
        withoutusermusic.purchase_permission = int(_newPermission)
        withoutusermusic.music_price = str(w3.fromWei(_money, "ether"))
        withoutusermusic.purchase_transactionHash = transactionHash
        withoutusermusic.save()
        if old_music:
            old_music = old_music.first()
            old_music.purchase_isUpdate = int(_id)
            old_music.purchase_status = 4
            old_music.save()
        else:
            oldwithoutusermusic = WitchoutUserMusic.objects.filter(purchase_bcId=str(_purchaseId))
            if oldwithoutusermusic:
                oldwithoutusermusic = oldwithoutusermusic.first()
                oldwithoutusermusic.purchase_isUpdate = int(_id)
                oldwithoutusermusic.save()


    else:
        if old_music:
            old_music = old_music.first()
            old_music.purchase_isUpdate = int(_id)
            old_music.purchase_status = 4
            old_music.save()
            usermusic = UserMusic()
            usermusic.user = owner.first()
            usermusic.purchase_transactionHash = transactionHash
            usermusic.purchase_bcId = str(_id)
            usermusic.purchase_permission = int(_newPermission)
            usermusic.purchase_status = 1
            usermusic.music_price = str(w3.fromWei(_money, "ether"))
            usermusic.timestamp = _timestamp
            usermusic.music = old_music.music
            usermusic.projectname = projectname.encode().decode("unicode-escape")
            usermusic.save()
        else:
            withoutusermusic = WitchoutUserMusic()
            withoutusermusic.bought_address = _form
            withoutusermusic.timestamp = _timestamp
            withoutusermusic.purchase_bcId = str(_id)
            withoutusermusic.purchase_permission = int(_newPermission)
            withoutusermusic.music_price = str(w3.fromWei(_money, "ether"))
            withoutusermusic.purchase_transactionHash = transactionHash
            withoutusermusic.save()
            oldwithoutusermusic = WitchoutUserMusic.objects.filter(purchase_bcId=str(_purchaseId))
            if oldwithoutusermusic:
                oldwithoutusermusic = oldwithoutusermusic.first()
                oldwithoutusermusic.purchase_isUpdate = int(_id)
                oldwithoutusermusic.save()


@shared_task
def refundTask(_address, _msg):
    refund_music = UserMusic.objects.filter(purchase_bcId=str(_msg)).filter(user__address=_address)
    if refund_music:
        refund_music = refund_music.first()
        old_music = UserMusic.objects.filter(user__address=_address).filter(
            purchase_isUpdate=refund_music.purchase_bcId)
        if old_music:
            old_music = old_music.last()
            old_music.purchase_isUpdate = old_music.purchase_bcId
            if old_music.purchase_status == 4:
                old_music.purchase_status = 2
            old_music.save()
        else:
            without_old_music = WitchoutUserMusic.objects.filter(purchase_isUpdate=refund_music.purchase_bcId).filter(
                bought_address=_address)
            if without_old_music:
                without_old_music = without_old_music.first()
                without_old_music.purchase_isUpdate = 0
                without_old_music.save()
        refund_music.purchase_status = 6
        refund_music.save()
    else:
        without_refund_music = WitchoutUserMusic.objects.filter(purchase_bcId=str(_msg)).filter(
            bought_address=_address).first()
        old_music = UserMusic.objects.filter(user__address=_address).filter(
            purchase_isUpdate=without_refund_music.purchase_bcId)
        if old_music:
            old_music = old_music.last()
            old_music.purchase_isUpdate = old_music.purchase_bcId
            if old_music.purchase_status == 4:
                old_music.purchase_status = 2
            old_music.save()
        else:
            without_old_music = WitchoutUserMusic.objects.filter(
                purchase_isUpdate=without_refund_music.purchase_bcId).filter(
                bought_address=_address)
            if without_old_music:
                without_old_music = without_old_music.first()
                without_old_music.purchase_isUpdate = 0
                without_old_music.save()
        without_refund_music.save()


@shared_task
def becomeproTask(_address):
    user = UserProfile.objects.filter(address=_address)
    if user:
        user = user.first()
        user.is_producter = True
        user.save()
    else:
        without_user = WithoutUserProfile.objects.filter(address=_address)
        if without_user:
            without_user = without_user.first()
            without_user.is_producter = True
            without_user.save()
        else:
            without_user = WithoutUserProfile()
            without_user.address = _address
            without_user.is_producter = True
            without_user.save()


@shared_task
def exitproTask(_address):
    user = UserProfile.objects.filter(address=_address)
    if user:
        user = user.first()
        user.is_producter = False
        user.save()
    else:
        without_user = WithoutUserProfile.objects.filter(address=_address)
        if without_user:
            without_user = without_user.first()
            without_user.is_producter = False
            without_user.save()


@shared_task
def flushTask():
    all_purchase = UserMusic.objects.filter(purchase_status=1)
    if all_purchase:
        for purchase in all_purchase:
            if purchase.check_upload():
                uploadKeyFile.apply_async(args=(purchase.user.address, purchase.user.publickey, purchase.purchase_bcId))
                purchase.key_ipfshash = "padding"
                purchase.save()


@shared_task
def checkVaildTask():
    all_purchase = UserMusic.objects.all()
    if all_purchase:
        for purchase in all_purchase:
            purchase.check_vaild()


@shared_task(base=QueueOnce, once={'graceful': True, 'timeout': 60 * 10})
def uploadKeyFile(address, publickey, purchase_bcId, music_bcId):
    request_data = {
        'type': 2,
        'address': address,
        'public': publickey,
        'purchase_bcId': purchase_bcId,
        'productId': music_bcId,
    }
    recvmsg = client.send_msg(request_data)
    if recvmsg == 'ok':
        bought_music = UserMusic.objects.filter(purchase_bcId=str(purchase_bcId))
        if bought_music:
            bought_music = bought_music.first()
            bought_music.purchase_status = 2
            bought_music.save()
            return 'upload key success'
        else:
            return "upload key fail code:101"

    else:
        return "upload key fail code:102"


@shared_task
def productSoldDetail(productId, address):
    temp = TemporaryFile('w+t', encoding='utf-8')
    temp.write('PurchaseID-CopyrightID-Permission-Timestmap-Price(Wei)-Buyer-address-Update' + '\n')
    all_sell = action.functions.getPurchaseIdByProduceId(int(productId)).call(
        {'from': keyring.get_password('DRMDEMO', 'address')})
    for sell in all_sell[1:]:
        information = action.functions.getPurchaseStorageById(sell).call(
            {'from': keyring.get_password('DRMDEMO', 'address')})
        temp.write(str(sell) + '----')
        temp.write('----'.join('%s' % id for id in information) + '\n')

    content = '尊敬的版权发布者，截止到%s时，您的版权ID为%s所售出的详细信息，请查收。' % (datetime.now(), productId)
    textApart = MIMEText(content)

    temp.seek(0)
    zipApart = MIMEApplication(temp.read())
    zipApart.add_header('Content-Disposition', 'attachment', filename='copyrightID_%s.txt' % (productId))

    m = MIMEMultipart()
    m.attach(textApart)
    m.attach(zipApart)
    m['Subject'] = Header('您的版权售卖详情——区块链音乐版权平台', 'utf-8')
    m['from'] = EMAIL_HOST_USER
    m['to'] = address
    try:
        server = smtplib.SMTP()
        server.connect(EMAIL_HOST, 25)
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, address, m.as_string())
        server.quit()
        temp.close()
        return 'email send success'
    except smtplib.SMTPException as e:
        temp.close()
        return 'email send error%s' % e


@shared_task
def receiveKeyTask(purchase_bcId, ipfshash):
    bought_music = UserMusic.objects.filter(purchase_bcId=str(purchase_bcId))
    if bought_music:
        bought_music = bought_music.first()
        ipfs_hash = action.functions.getLicenseBypurchaseId(int(bought_music.purchase_bcId)).call(
            {'from': keyring.get_password('DRMDEMO', 'address')})
        if str(ipfs_hash) == str(ipfshash):
            bought_music.key_ipfshash = ipfshash
            bought_music.save()
        else:
            return 'receive key error 102'
    else:
        return 'receive key error 101'


@shared_task
def sendKey(id, ipfshash, address):
    temp = TemporaryFile('w+b')
    bytes_key = ipfsclient.cat(str(ipfshash))
    temp.write(bytes_key)
    content = '尊敬的版权购买者，这是您购买的id为%s版权，请查收。' % (id)
    textApart = MIMEText(content)

    temp.seek(0)
    zipApart = MIMEApplication(temp.read())
    zipApart.add_header('Content-Disposition', 'attachment', filename='%s_%s.key' % (id, ipfshash))

    m = MIMEMultipart()
    m.attach(textApart)
    m.attach(zipApart)
    m['Subject'] = Header('您的版权密钥——区块链音乐版权平台', 'utf-8')
    m['from'] = EMAIL_HOST_USER
    m['to'] = address
    try:
        server = smtplib.SMTP()
        server.connect(EMAIL_HOST, 25)
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, address, m.as_string())
        server.quit()
        temp.close()
        return 'email send success'
    except smtplib.SMTPException as e:
        temp.close()
        return 'email send error%s' % e
