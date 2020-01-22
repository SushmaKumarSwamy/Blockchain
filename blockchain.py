# blockchain= [1]

# def add_value():
#     blockchain.append([blockchain[-1],5.3])
#     print(blockchain)

# add_value()
# add_value()
# add_value()

# blockchain= []

# def get_last_blockchain_value():
#     return blockchain[-1]

# def add_value(transaction_amount, last_transaction=[1]):
#     blockchain.append([last_transaction,transaction_amount])

# add_value(2)
# add_value(0.9,get_last_blockchain_value())
# add_value(10.9, get_last_blockchain_value())

# print(blockchain)
genesis_block={
    'previous_hash' : '',
    'index': 0,
    'transactions': []
}
blockchain= [genesis_block]
open_transaction = []
owner = 'Sush'


def get_last_blockchain_value():
    """ returns the last elemet of the blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def mine_block():
    last_block = blockchain[-1]
    hashed_block = ''
    for keys in last_block:
        value = last_block[keys]
        hashed_block = hashed_block + str(value)
    print(hashed_block)
    block = {'previous_hash' : 'XYZ',
    'index': len(blockchain),
    'transactions': open_transaction
    }
    blockchain.append(block)


def add_transaction(recipient,sender = owner,amount=1.0):
    """ blockchain will be appended with new transaction and previous transaction
    Arguments 
        sender: the sender of coins
        recipient: the recipient of the coin
        amount: the amount of coins sent with the transaction
        
         """
    transcation = {'sender': sender,
                    'recipient': recipient,
                    'amount': amount
                    }
    open_transaction.append(transcation)

def get_choice():
    choice = input('enter your choice')
    return choice

def get_transaction_value():
    """ takes new transaction input from the user as a float"""
    tx_receipient = input('enter the recipient of the transaction')
    tx_amount = input('enter the amount you want to send')
    
    return tx_receipient, tx_amount


def print_blocks():
    for block in blockchain:
        print(block)

def block_verify():
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index -1]:
            is_valid = True
        else: 
            is_valid = False
            break
    # block_index = 0
    # is_valid = True

    # for block in blockchain:
    #     if block_index == 0:
    #         block_index +=1
    #     elif block[0] == blockchain[block_index - 1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    return is_valid

while True:
    print('Choose:')
    print('1: Add value to the blockchain')
    print('2 : Mine Block')
    print('3: print the blocks')
    print('4: manipulate')
    print('q: Quit')
    choice = get_choice()
    if choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient,amount=amount)
        print(open_transaction)
    elif choice == '2':
        mine_block()
    elif choice == '3':
        print_blocks()
    elif choice == '4':
        if len(blockchain) >= 1:
            blockchain[0] =[2]
    elif choice == 'q':
        break
    # if not block_verify():
    #     print('invalid chain')
    
print("done")