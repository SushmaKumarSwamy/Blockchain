from functools import reduce
import hashlib as hl

import json
import pickle

from block import Block
from transaction import Transaction
from hash_util import hash_block
from verification import Verification

MINING_REWARD = 10
# the origianl blockchain


class Blockchain:
    def __init__(self,hosting_node_id):
        genesis_block = Block(0,'',[],100,0)
        self.chain = [genesis_block]
        self.__open_transaction = []
        self.load_data()
        self.hosting_node = hosting_node_id
    @property
    def chain (self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val


    def get_open_transaction(self):
        return self.__open_transaction[:]

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                
                # blockchain = file_content['chain']
                # open_transaction =file_content['ot']
            
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'],block['previous_hash'],converted_tx ,block['proof'],block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transaction = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transaction:
                    updated_transaction = Transaction(tx['sender'],tx['recipient'],tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transaction = updated_transactions
        except (IOError, IndexError):
            print('error handled...')


    # saving the data to the file
    def save_data(self):
        """Save blockchain + open transactions snapshot to a file."""
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions],block_el.proof,block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transaction]
                f.write(json.dumps(saveable_tx))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed!') 



    # generating hashes for the block
    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0 
        while not Verification.valid_proof(self.__open_transaction, last_hash,proof):
            proof +=1
        return proof


    # to get the balance of the participants as of now the owner!
    def get_balance(self):
        
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [ tx.amount for tx in self.__open_transaction if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_sender,0)
        
        tx_receipient=  [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum,tx_amt:tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_receipient,0)
    
        return amount_received - amount_sent


    # to get the last block of the blockchain
    def get_last_blockchain_value(self):
        """ returns the last elemet of the blockchain"""
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]



    # adding transaction to the pool
    def add_transaction(self,recipient,sender,amount=1.0):
        """ blockchain will be appended with new transaction and previous transaction
        Arguments 
            sender: the sender of coins
            recipient: the recipient of the coin
            amount: the amount of coins sent with the transaction
        """
        trx = Transaction(sender,recipient,amount)
        if Verification.verify_transaction(trx,self.get_balance):
            self.__open_transaction.append(trx)
            self.save_data()
            return True
        return False




    # mining the block i.e adding thr transaction from opent pool to block
    def mine_block(self):
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING',self.hosting_node,MINING_REWARD)
        copied_transactions = self.__open_transaction[:]
        copied_transactions.append(reward_transaction)
        # check while passing the variables(names) in the function
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transaction =[]
        self.save_data()
        return True





