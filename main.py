import blockchain as b
import json

def main():

	state = {u'Alice':50,u'Bob':50}
	genesisBlockTxns = [state]
	genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns}
	genesisHash = b.hashMe(genesisBlockContents)
	genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
	genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)

	chain = [genesisBlock] #first block

	blockSizeLimit = b.blockSizeLimit() ########### GUI CONNECTION ###########

	transactions = b.howManyTxnsPerBlock() ########### GUI CONNECTION ###########

	while blockSizeLimit < transactions:
		print('ERROR: YOUR BLOCK SIZE LIMIT CANNOT BE SMALLER THAN TXNS!\n')
		transactions = b.howManyTxnsPerBlock()

	txnBuffer = [b.makeTransaction() for i in range(transactions)] 

	while len(txnBuffer) > 0:
		bufferStartSize = len(txnBuffer)
		txnList = []
		while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
			newTxn = txnBuffer.pop()
			validTxn = b.isValidTxn(newTxn,state)

			if validTxn:
				txnList.append(newTxn)
				state = b.updateState(newTxn,state)
			else:
				print('Ignored transaction')
				sys.stdout.flush()
				continue

	x = input('NUMBER OF BLOCKS:\n') ########### GUI CONNECTION ###########
	for i in range(int(x)):
		newBlock = b.makeBlock(txnList,chain)
		chain.append(newBlock)

	chainAsText = json.dumps(chain,sort_keys=True) #Dumps all data in chain

	option = input('PRESS 1 TO PRINT WHOLE CHAIN\nPRESS 2 TO PRINT HASH OF CHAIN\n')
	if option == '1':
		b.printWholeChain(chain)
	elif option == '2':
		b.printChainsHash(chain)
	else:
		print("COULDN'T PRINT ANYTHING")	

main()
