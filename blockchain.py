from functools import reduce
import hashlib as hl
from collections import OrderedDict
import json
import pickle

from block import Block
from hash_util import hash_string_256, hash_block



# mining reward for the minners
MINING_REWARD = 10
# the origianl blockchain
blockchain= []
# transaction in pool
open_transaction = []

# person incharge of this node
owner = 'Sush'
# overall view of the participants involved in this blockchain
participants = { 'Sush' }

def load_data():
    global blockchain
    global open_transaction
    try:
        with open('blockchain.txt', mode='r') as f:
            file_content = f.readlines()
            
            # blockchain = file_content['chain']
            # open_transaction =file_content['ot']
        
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [OrderedDict([('sender',tx['sender']),('recipient',tx['recipient']),('amount',tx['amount'])]) for tx in block['transactions']]
                updated_block = Block(block['index'],block['previous_hash'],converted_tx ,block['proof'],block['timestamp'])
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transaction = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transaction:
                updated_transaction = OrderedDict([('sender',tx['sender']),('recipient',tx['recipient']),('amount',tx['amount'])])
                updated_transactions.append(updated_transaction)
            open_transaction = updated_transactions
    except (IOError, IndexError):
        genesis_block = Block(0,'',[],100,0)
        blockchain= [genesis_block]
        open_transaction = []

load_data()

# saving the data to the file
def save_data():
    """Save blockchain + open transactions snapshot to a file."""
    try:
        with open('blockchain.txt', mode='w') as f:
            saveable_chain = [block.__dict__ for block in blockchain]
            f.write(json.dumps(saveable_chain))
            f.write('\n')
            f.write(json.dumps(open_transaction))
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving failed!') 


# checking which hash is the 'one' based on the complexity
def valid_proof(transactions,last_hash,proof):
    guess = (str(transactions)+ str(last_hash)+str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2]=='00'

# generating hashes for the block
def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0 
    while not valid_proof(open_transaction, last_hash,proof):
        proof +=1
    return proof


# to get the balance of the participants as of now the owner!
def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block.transactions if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [ tx['amount'] for tx in open_transaction if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_sender,0)
    
    tx_receipient=  [[tx['amount'] for tx in block.transactions if tx['recipient'] == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum,tx_amt:tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_receipient,0)
  
    return amount_received - amount_sent


# to get the last block of the blockchain
def get_last_blockchain_value():
    """ returns the last elemet of the blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

# to check whether the user has sufficient balance to send the money he intend to do 
def verify_transaction(transaction):
    sender_balance= get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

# adding transaction to the pool
def add_transaction(recipient,sender = owner,amount=1.0):
    """ blockchain will be appended with new transaction and previous transaction
    Arguments 
        sender: the sender of coins
        recipient: the recipient of the coin
        amount: the amount of coins sent with the transaction
    """
    trx = OrderedDict(
        [('sender',sender),('recipient',recipient),('amount',amount)]
    )
    if verify_transaction(trx):
        open_transaction.append(trx)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False




# mining the block i.e adding thr transaction from opent pool to block
def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = OrderedDict(
        [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
    copied_transactions = open_transaction[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True

# to fetch the user values
def get_transaction_value():
    """ takes new transaction input from the user as a float"""
    tx_receipient = input('enter the recipient of the transaction')
    tx_amount = float(input('enter the amount you want to send'))
    return tx_receipient, tx_amount


# to take what user wants to do
def get_choice():
    choice = input('enter your choice')
    return choice


#print blocks:)
def print_blocks():
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)

# just to check all the transactions in open transaction are valid!
def verify_transactions():
    print(open_transaction)
    return all([verify_transaction(tx) for tx in open_transaction])




# to check the blockchain is not tampered with some false data
def block_verify():
    for (index, block) in enumerate(blockchain):
        if index == 0 :
            continue
        if block.previous_hash != hash_block(blockchain[index-1]):
            return False
        if not valid_proof(block.transactions[:-1],block.previous_hash,block.proof):
            print('proof of work is invalid')
            return False
    return True


# loading the data from the file before starting the blockchain


# user interface 
while True:
    print('Choose:')
    print('1: Add value to the blockchain')
    print('2 : Mine Block')
    print('3: print the blocks')
    print('5: participants')
    print('6: check transaction validity on open transaction')
    print('q: Quit')
    choice = get_choice()
    if choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient,amount=amount):
            print('transaction added!!')
        else:
            print('transaction failed!')
    elif choice == '2':
        if mine_block():
            open_transaction = []
            save_data()
        # print(blockchain)
    elif choice == '3':
        print_blocks()
    elif choice == '5': 
        print(participants)
    elif choice == '6':
        if verify_transactions():
            print('transactions are valid')
        else:
            print('transactions are not valid')
    elif choice == 'q':
        break
    else:
        print('input was invalid, check from the list')
    if not block_verify():
        print('invalid chain')
        break
    print('Balance of {} is : {:6.2f}'.format('Sush',get_balance('Sush')))
else:
    print('user left')

print("done")