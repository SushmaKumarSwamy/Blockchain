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

blockchain= []

def get_last_blockchain_value():
    """ returns the last elemet of the blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_value(transaction_amount, last_transaction):
    """ blockchain will be appended with new transaction and previous transaction
    Arguments 
        :transaction_amount : new transaction to the block
        :last_transaction : the last block """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction,transaction_amount])

def get_choice():
    choice = input('enter your choice')
    return choice

def get_transaction_value():
    """ takes new transaction input from the user as a float"""
    return float(input('enter your transcation amount'))


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
    print('2: print the blocks')
    print('3: manipulate')
    print('q: Quit')
    choice = get_choice()
    if choice == '1':
        txt_amount = get_transaction_value()
        add_value(txt_amount,get_last_blockchain_value())
    elif choice == '2':
        print_blocks()
    elif choice == '3':
        if len(blockchain) >= 1:
            blockchain[0] =[2]
    elif choice == 'q':
        break
    if not block_verify():
        print('invalid chain')
    
print("done")