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
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    """ blockchain will be appended with new transaction and previous transaction
    Arguments 
        :transaction_amount : new transaction to the block
        :last_transaction : the last block """
    blockchain.append([last_transaction,transaction_amount])


def user_input():
    """ takes new transaction input from the user as a float"""
    return float(input('enter your transcation amount'))


txt_amount = user_input()
add_value(txt_amount)

txt_amount = user_input()
add_value(txt_amount,get_last_blockchain_value())

txt_amount = user_input()
add_value(txt_amount, get_last_blockchain_value())

print(blockchain)