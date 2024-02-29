from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from datetime import date
import datetime
import json
from web3 import Web3, HTTPProvider
import ipfsApi
import os
import pickle
import json
from web3 import Web3, HTTPProvider
from django.core.files.storage import FileSystemStorage
import pickle
import random
import pyaes, pbkdf2, binascii, os, secrets
import base64
import time
import matplotlib.pyplot as plt
import mimetypes
import numpy as np
api = ipfsApi.Client(host='http://127.0.0.1', port=5001)
global details
runtime_data = []
global blk
blk=0
global vrfy
vrfy=False
def getKey(): #generating key with PBKDF2 for AES
    password = "s3cr3t*c0d3"
    passwordSalt = '76895'
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    return key
def encrypt(plaintext): #AES data encryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

def decrypt(enc): #AES data decryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    decrypted = aes.decrypt(enc)
    return decrypted


def readDetails():
    global details
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'ForensicEvidenceContract.json' #forensic contract code
    deployed_contract_address = '0xa738B9C62832bc7F0639cb926873afa68d15d4bC' #hash address to access forensiccontract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    details = contract.functions.getData().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]

def saveDataBlockChain(currentData):
    global details
    global contract
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'ForensicEvidenceContract.json'
    deployed_contract_address = '0xa738B9C62832bc7F0639cb926873afa68d15d4bC'
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails()
    details+=currentData
    msg = contract.functions.setEvidenceDetails(details).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Admin(request):
    if request.method == 'GET':
       return render(request, 'Admin.html', {})
def Police(request):
    if request.method == 'GET':
       return render(request, 'Police.html', {})
def Hospital(request):
    if request.method == 'GET':
       return render(request, 'Hospital.html', {})
def User(request):
    if request.method == 'GET':
       return render(request, 'User.html', {})


def AddEvidence(request):
    if request.method == 'GET':
       return render(request, 'AddEvidence.html', {})

def AdminLogin(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      if username == 'admin' and password == 'admin':
       context= {'data':'welcome '+username}
       return render(request, 'AdminScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'Admin.html', context)
def PoliceLogin(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      if username == 'police' and password == 'police':
       context= {'data':'welcome '+username}
       return render(request, 'PoliceScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'Police.html', context)
def UserLogin(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      if username == 'lawyer' and password == 'lawyer':
       context= {'data':'welcome '+username}
       return render(request, 'UserScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'User.html', context)
def HospitalLogin(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      if username == 'doctor' and password == 'doctor':
       context= {'data':'welcome '+username}
       return render(request, 'HospitalScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'Hospital.html', context)
def Download(request):
    if request.method == 'GET':
        filename = request.GET['t1']
        hashcode = request.GET['t2']
        content = api.get_pyobj(hashcode)
        content = pickle.loads(content)
        content = decrypt(content)
        mime_type, _ = mimetypes.guess_type(filename)
        response = HttpResponse(content, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response  

def ViewEvidence(request):
    if request.method == 'GET':
        global details
        global blk
        readDetails()
        print("p det "+details)
        arr = details.split("\n")
        output = '<table class="table" id="myTable" data-filter-control="true" data-show-search-clear-button="true" border=1 align=center width=100% ><tr><th><font size="" color="black">Record ID</th><th><font size="" color="black">Crime Type</th><th><font size="" color="black">Description</th><th><font size="" color="black">Evidence</th><th><font size="" color="black">Witness</th><th><font size="" color="black">File Name</th>'
        output+='<th><font size="" color="black">Upload Date Time</th>'
        output+='<th><font size="" color="black">Blockchain Hash Value</th>'
        output+='<th><font size="" color="black">Download & View Data</th></tr>'
        files = []
        for i in range(len(arr)-1):
            array = arr[i].split("$")
            output+='<tr><td><font size="" color="black">'+str(array[0])+'</td>'
            output+='<td><font size="" color="black">'+str(array[1])+'</td>'
            output+='<td><font size="" color="black">'+str(array[2])+'</td>'
            output+='<td id="url"><font size="" color="black">'+str(array[3])+'</a></td>'
            output+='<td><font size="" color="black">'+str(array[4])+'</td>'
            output+='<td><font size="" color="black">'+str(array[5])+'</td>'
            output+='<td><font size="" color="black">'+str(array[6])+'</td>'
            output+='<td><font size="" color="black">'+str(array[7])+'</td>'
            output+='<td><a href="Download?t1='+array[5]+'&t2='+array[7]+'"><font size="" color="black">Click Here</a></td>'
        context= {'data':output}
        
        blk+=1
        print(str(blk) + " : Total blocks")
        return render(request, 'ViewEvidence.html', context)
def PViewEvidence(request):
    if request.method == 'GET':
        global details
        global blk
        global vrfy
        readDetails()
        print("p det "+details)
        arr = details.split("\n")
        output = '<table class="table" id="myTable" data-filter-control="true" data-show-search-clear-button="true" border=1 align=center width=100% ><tr><th><font size="" color="black">Record ID</th><th><font size="" color="black">Crime Type</th><th><font size="" color="black">Description</th><th><font size="" color="black">Evidence</th><th><font size="" color="black">Witness</th><th><font size="" color="black">File Name</th>'
        output+='<th><font size="" color="black">Upload Date Time</th>'
        output+='<th><font size="" color="black">Blockchain Hash Value</th>'
        output+='<th><font size="" color="black">Download & View Data</th></tr>'
        files = []
        for i in range(len(arr)-1):
            array = arr[i].split("$")
            output+='<tr><td><font size="" color="black">'+str(array[0])+'</td>'
            output+='<td><font size="" color="black">'+str(array[1])+'</td>'
            output+='<td><font size="" color="black">'+str(array[2])+'</td>'
            output+='<td id="url><font size="" color="black">'+str(array[3])+'</td>'
            output+='<td><font size="" color="black">'+str(array[4])+'</td>'
            output+='<td><font size="" color="black">'+str(array[5])+'</td>'
            output+='<td><font size="" color="black">'+str(array[6])+'</td>'
            output+='<td><font size="" color="black">'+str(array[7])+'</td>'
            output+='<td><a href="Download?t1='+array[5]+'&t2='+array[7]+'"><font size="" color="black">Click Here</a></td>'
            
        context= {'data':output}
        
        blk+=1
        print(str(blk) + " : Total blocks")
        return render(request, 'PViewEvidence.html', context)  
def HViewEvidence(request):
    if request.method == 'GET':
        global details
        global blk
        readDetails()
        print("p det "+details)
        arr = details.split("\n")
        output = '<table class="table" id="myTable" data-filter-control="true" data-show-search-clear-button="true" border=1 align=center width=100% ><tr><th><font size="" color="black">Record ID</th><th><font size="" color="black">Crime Type</th><th><font size="" color="black">Description</th><th><font size="" color="black">Evidence</th><th><font size="" color="black">Witness</th><th><font size="" color="black">File Name</th>'
        output+='<th><font size="" color="black">Upload Date Time</th>'
        output+='<th><font size="" color="black">Blockchain Hash Value</th>'
        output+='<th><font size="" color="black">Download & View Data</th></tr>'
        files = []
        for i in range(len(arr)-1):
            array = arr[i].split("$")
            output+='<tr><td><font size="" color="black">'+str(array[0])+'</td>'
            output+='<td><font size="" color="black">'+str(array[1])+'</td>'
            output+='<td><font size="" color="black">'+str(array[2])+'</td>'
            output+='<td id="url><font size="" color="black">'+str(array[3])+'</td>'
            output+='<td><font size="" color="black">'+str(array[4])+'</td>'
            output+='<td><font size="" color="black">'+str(array[5])+'</td>'
            output+='<td><font size="" color="black">'+str(array[6])+'</td>'
            output+='<td><font size="" color="black">'+str(array[7])+'</td>'
            output+='<td><a href="Download?t1='+array[5]+'&t2='+array[7]+'"><font size="" color="black">Click Here</a></td>'
        context= {'data':output}
        
        blk+=1
        print(str(blk) + " : Total blocks")
        return render(request, 'HViewEvidence.html', context)

def UViewEvidence(request):
    if request.method == 'GET':
        global details
        global blk
        readDetails()
        print("p det "+details)
        arr = details.split("\n")
        output = '<table class="table" id="myTable" data-filter-control="true" data-show-search-clear-button="true" border=1 align=center width=100% ><tr><th><font size="" color="black">Record ID</th><th><font size="" color="black">Crime Type</th><th><font size="" color="black">Description</th><th><font size="" color="black">Evidence</th><th><font size="" color="black">Witness</th><th><font size="" color="black">File Name</th>'
        output+='<th><font size="" color="black">Upload Date Time</th>'
        output+='<th><font size="" color="black">Blockchain Hash Value</th>'
        output+='<th><font size="" color="black">Download & View Data</th></tr>'
        files = []
        for i in range(len(arr)-1):
            array = arr[i].split("$")
            output+='<tr><td><font size="" color="black">'+str(array[0])+'</td>'
            output+='<td><font size="" color="black">'+str(array[1])+'</td>'
            output+='<td><font size="" color="black">'+str(array[2])+'</td>'
            output+='<td id="url><font size="" color="black">'+str(array[3])+'</td>'
            output+='<td><font size="" color="black">'+str(array[4])+'</td>'
            output+='<td><font size="" color="black">'+str(array[5])+'</td>'
            output+='<td><font size="" color="black">'+str(array[6])+'</td>'
            output+='<td><font size="" color="black">'+str(array[7])+'</td>'
            output+='<td><a href="Download?t1='+array[5]+'&t2='+array[7]+'"><font size="" color="black">Click Here</a></td>'
        context= {'data':output}
        
        blk+=1
        print(str(blk) + " : Total blocks")
        return render(request, 'UViewEvidence.html', context)     

def AddEvidenceAction(request):

    if request.method == 'POST':
        rid = request.POST.get('t5', False)
        crime_type = request.POST.get('t2', False)
        desc = request.POST.get('t3', False)
        evidence = request.POST.get('t4', False)
        witness = request.POST.get('t6', False)
        filename = request.FILES['t1'].name
        myfile = request.FILES['t1'].read()
        myfile = encrypt(myfile)
        myfile = pickle.dumps(myfile)
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        hashcode = api.add_pyobj(myfile)
        today = date.today()
        data = rid+"$"+crime_type+"$"+desc+"$"+evidence+"$"+witness+"$"+str(filename)+"$"+str(today)+"$"+str(hashcode)+"\n"
        saveDataBlockChain(data)
        output = 'Given Evidence file saved in blockchain with hash code.<br/>'+str(hashcode)
        context= {'data':'Your Forensic Evidences is safe and added to the BlockChain '}
        blk=1
        print( str(blk) + " Block created and added")
        return render(request, 'AddEvidence.html', context) 

def About(request):
   if request.method == 'GET':
      return render(request, 'Site1/About.html') 

def Contact(request):
   if request.method == 'GET':
      return render(request, 'Site1/Contact.html') 












        
