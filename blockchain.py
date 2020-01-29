from functools import reduce
import hashlib as hl
from collections import OrderedDict


from hash_util import hash_string_256, hash_block


genesis_block={
    'previous_hash' : '',
    'index': 0,
    'transactions': [],
    'proof':100
}

MINING_REWARD = 10
blockchain= [genesis_block]
open_transaction = []
owner = 'Sush'
participants = { 'Sush' }




def get_last_blockchain_value():
    """ returns the last elemet of the blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [ tx['amount'] for tx in open_transaction if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_sender,0)
    
    tx_receipient=  [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum,tx_amt:tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_receipient,0)
  
    return amount_received - amount_sent


def valid_proof(transactions,last_hash,proof):
    guess = (str(transactions)+ str(last_hash)+str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2]=='00'

def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0 
    while not valid_proof(open_transaction, last_hash,proof):
        proof +=1
    return proof

def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount':MINING_REWARD
    # }
    reward_transaction = OrderedDict(
        [('sender', 'MINING'),('recipient',owner),('amount',MINING_REWARD)]
    )
    copied_transactions = open_transaction[:]
    copied_transactions.append(reward_transaction)
    block = {'previous_hash' : hashed_block,
            'index': len(blockchain),
            'transactions': copied_transactions,
            'proof':proof
            }
    blockchain.append(block)
    return True


def add_transaction(recipient,sender = owner,amount=1.0):
    """ blockchain will be appended with new transaction and previous transaction
    Arguments 
        sender: the sender of coins
        recipient: the recipient of the coin
        amount: the amount of coins sent with the transaction
    """
    # trx = { 'sender': sender,
    #         'recipient': recipient,
    #         'amount': amount
    #     }
    trx = OrderedDict(
        [('sender',sender),('recipient',recipient),('amount',amount)]
    )
    if verify_transaction(trx):
        open_transaction.append(trx)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def verify_transaction(transaction):
    sender_balance= get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def verify_transactions():
    print(open_transaction)
    return all([verify_transaction(tx) for tx in open_transaction])


def get_choice():
    choice = input('enter your choice')
    return choice


def get_transaction_value():
    """ takes new transaction input from the user as a float"""
    tx_receipient = input('enter the recipient of the transaction')
    tx_amount = float(input('enter the amount you want to send'))
    return tx_receipient, tx_amount


def print_blocks():
    for block in blockchain:
        print(block)


def block_verify():
    for (index, block) in enumerate(blockchain):
        if index == 0 :
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
        if not valid_proof(block['transactions'][:-1],block['previous_hash'],block['proof']):
            print('proof of wprk is invalid')
            return False
    return True


while True:
    print('Choose:')
    print('1: Add value to the blockchain')
    print('2 : Mine Block')
    print('3: print the blocks')
    print('4: manipulate')
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
        # print(blockchain)
    elif choice == '3':
        print_blocks()
    elif choice == '4':
        if len(blockchain) >= 1:
            blockchain[0] ={
                            'previous_hash' : '',
                            'index': 0,
                            'transactions': {'sender': 'mimi', 'recepient' : 'jojo', 'amount': 10}
                            }
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