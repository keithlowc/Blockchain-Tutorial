#!/usr/bin/python3

import hashlib, json, random, sys
import copy

def hashMe(msg=""):
	if type(msg) != str:
		msg = json.dumps(msg,sort_keys=True)
	if sys.version_info.major == 2: #version 2.0
		return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')
	else:
		return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

## Random 
random.seed(0)

def makeTransaction(maxValue=3):
	sign = int(random.getrandbits(1))*2-1 #Creates random -1 or 1
	amount = random.randint(1,maxValue)   #Random number from 1 to max
	alicePays = sign * amount
	bobPays = -1 * alicePays
	return {u'Alice':alicePays,u'Bob':bobPays}

def updateState(txn,state):
	state = state.copy()

	for key in txn:
		if key in state.keys():
			state[key] += txn[key]
		else:
			state[key] = txn[key]

	return state


def isValidTxn(txn,state):
	if sum(txn.values()) is not 0: #the sum of all transactions should be zero
		return False
	for key in txn.keys():
		if key in state.keys():
			acctBalance = state[key]
		else:
			acctBalance = 0
		if (acctBalance + txn[key]) < 0:
			msg = 'Transaction is not valid'
			print(msg)
			return False
	return True

## Example of different transactions
def exampleTransactions():
	state = {u'Alice':5,u'Bob':5}
	print(isValidTxn({u'Alice': -3,u'Bob': 3},state)) #True
	print(isValidTxn({u'Alice': -4,u'Bob': 3},state)) #False
	print(isValidTxn({u'Alice': -6,u'Bob': 6},state)) #True
	print(isValidTxn({u'Alice': -4,u'Bob': 2,'Lisa':2},state)) #True
	print(isValidTxn({u'Alice': -4,u'Bob': 3,'Lisa':2},state)) #False

def makeBlock(txns,chain):
	parentBlock = chain[-1]
	parentHash = parentBlock[u'hash']
	blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
	txnCount = len(txns)
	blockContents = {u'blockNumber':blockNumber,u'parentHash':parentHash,u'txnCount':txnCount,u'txns':txns}
	blockHash = hashMe(blockContents)
	block = {u'contents':blockContents,u'hash':blockHash}

	return block

def checkBlockHash(block):
	expectedHash = hashMe(block['contents'])
	if block['hash'] != expectedHash:
		raise Exception('Hash does not match contents of block %s'% block['contents']['blockNumber'])
	return

def checkBlockValidity(block,parent,state):
	parentNumber = parent['contents']['blockNumber']
	parentHash = parent['hash']
	blockNumber = block['contents']['blockNumber']

	for txn in block['contents']['txns']:
		if isValidTxn(txn,state): #if valid returns True
			state = updateState(txn,state)
		else:
			raise Exception('Invalid transaction in block %s: %s'%(blockNumber,tx))

	checkBlockHash(block) #if invalid raises exception

	if blockNumber != (parentNumber + 1):
		raise Exception('Hash does not match contents of block %s'%blockNumber)
	if block['contents']['parentHash'] != parentHash:
		raise Exception('Parent hash not accurate at block %s'%blockNumber)
	return state

def checkChain(chain):
	if type(chain) == str:
		try:
			chain = json.loads(chain)
			assert(type(chain) == list) #Assert checks that chain is a list
		except:
			return False
	elif type(chain) != list:
		return False

	state = {}

	for txn in chain[0]['contents']['txns']: #Checks genesis block
		state = updateState(txn,state) 		 #Transactions are valid
	checkBlockHash(chain[0])				 #Block hash is valid for block contents
	parent = chain[0]

	for block in chain[1:]:
		state = checkBlockValidity(block,parent,state)
		parent = block
	return state

def printWholeChain(chain):
	for x in range(len(chain)):
		print('++++++++ START OF BLOCK # ' + str(x) + ' ++++++')
		print(str(chain[x]))
		print('++++++++ END OF BLOCK # ' + str(x) + ' ++++++++\n')

def printChainsHash(chain):
	print('++++++ PRINTING BLOCK HASHES +++++++++++++')
	for i in range(len(chain)):
		chainHash = chain[i]['hash']
		print(str(i)+'- ' + str(chainHash))
	print('++++++ END OF PRINTING BLOCK HASHES ++++++')

def hello():
	print('Hello')

def blockSizeLimit():
	x = input('MAX TRANSACTIONS ALLOWED PER BLOCK?:\n')
	return int(x) 

def howManyTxnsPerBlock():
	x = input('NUMBER OF RANDOM TRANSACTIONS IN EACH BLOCK:\n')
	return int(x)



