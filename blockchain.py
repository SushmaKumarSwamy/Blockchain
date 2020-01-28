genesis_block={
    'previous_hash' : '',
    'index': 0,
    'transactions': []
}

MINING_REWARD = 25
blockchain= [genesis_block]
open_transaction = []
owner = 'Sush'
participants = { 'Sush' }


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_last_blockchain_value():
    """ returns the last elemet of the blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [ tx['amount'] for tx in open_transaction if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) >0:
            amount_sent += tx[0]
    tx_receipient=  [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_receipient:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent

def mine_block():
    print('before mining---------',blockchain)
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount':MINING_REWARD
    }
    open_transaction.append(reward_transaction)
    block = {'previous_hash' : hashed_block,
            'index': len(blockchain),
            'transactions': open_transaction
            }
    blockchain.append(block)
    print('after mining---------',blockchain)
    return True


def add_transaction(recipient,sender = owner,amount=1.0):
    """ blockchain will be appended with new transaction and previous transaction
    Arguments 
        sender: the sender of coins
        recipient: the recipient of the coin
        amount: the amount of coins sent with the transaction
    """
    trx = { 'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
    if verify_transaction(trx):
        open_transaction.append(trx)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def verify_transaction(transaction):
    sender_balance= get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def get_choice():
    choice = input('enter your choice')
    return choice


def get_transaction_value():
    """ takes new transaction input from the user as a float"""
    tx_receipient = input('enter the recipient of the transaction')
    tx_amount = int(input('enter the amount you want to send'))
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
    return True


while True:
    print('Choose:')
    print('1: Add value to the blockchain')
    print('2 : Mine Block')
    print('3: print the blocks')
    print('4: manipulate')
    print('5: participants')
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
    elif choice == 'q':
        break
    else:
        print('input was invalid, check from the list')
    if not block_verify():
        print('invalid chain')
        break
    print(get_balance('Sush'))
else:
    print('user left')

print("done")