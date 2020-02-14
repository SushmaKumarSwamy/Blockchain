from uuid import uuid4

from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet


class Node:
    def __init__(self):
       #self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)


    # to fetch the user values
    def get_transaction_value(self):
        """ takes new transaction input from the user as a float"""
        tx_receipient = input('enter the recipient of the transaction')
        tx_amount = float(input('enter the amount you want to send'))
        return tx_receipient, tx_amount


    # to take what user wants to do
    def get_choice(self):
        choice = input('enter your choice')
        return choice


    #print blocks:)
    def print_blocks(self):
        for block in self.blockchain.chain:
            print('Outputting Block')
            print(block)
        else:
            print('-' * 20)

    def listen_to_input(self):
        while True:
            print('Choose:')
            print('1: Add value to the blockchain')
            print('2 : Mine Block')
            print('3: print the blocks')
            print('4: Create wallet')
            print('5: load Wallet')
            print('6: check transaction validity on open transaction')
            print('q: Quit')
            choice = self.get_choice()
            if choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient,self.wallet.public_key, amount=amount):
                    print('transaction added!!')
                else:
                    print('transaction failed!')
                print(self.blockchain.get_open_transaction)
            elif choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed. Got no wallet')
                    
                # print(blockchain)
            elif choice == '3':
                self.print_blocks()
            elif choice == '4':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif choice == '5':
                pass
            elif choice == '6':
                if Verification.verify_transactions(self.blockchain.get_open_transaction(),self.blockchain.get_balance):
                    print('transactions are valid')
                else:
                    print('transactions are not valid')
            elif choice == 'q':
                break
            else:
                print('input was invalid, check from the list')

            if not Verification.block_verify(self.blockchain.chain):
                print('invalid chain')
                break
            print('Balance of {} is : {:6.2f}'.format(self.wallet.public_key,self.blockchain.get_balance()))
        else:
            print('user left')

        print("done")

# telling pyhton to execute the node.py file only when its is executed. if its imported any other file and that file is running, no need to run this
node = Node()
node.listen_to_input()