from functools import reduce
import hashlib as hl

import json
import pickle
import requests

from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet


MINING_REWARD = 10
# the origianl blockchain


class Blockchain:
    def __init__(self,public_key, node_id):
        genesis_block = Block(0,'',[],100,0)
        self.chain = [genesis_block]
        self.__open_transaction = []
        self.public_key = public_key
        self.__peer_nodes = set()
        self.node_id= node_id
        self.load_data()


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
            with open('blockchain-{}.txt'.format(self.node_id), mode='r') as f:
                file_content = f.readlines()
                
                # blockchain = file_content['chain']
                # open_transaction =file_content['ot']
            
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'],block['previous_hash'],converted_tx ,block['proof'],block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transaction = json.loads(file_content[1][:-1])
                updated_transactions = []
                for tx in open_transaction:
                    updated_transaction = Transaction(tx['sender'],tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transaction = updated_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes= set(peer_nodes)
        except (IOError, IndexError):
            print('error handled...')


    # saving the data to the file
    def save_data(self):
        """Save blockchain + open transactions snapshot to a file."""
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions],block_el.proof,block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transaction]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
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
    def get_balance(self, sender=None):
        
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
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
    def add_transaction(self,recipient,sender, signature, amount=1.0, is_receiving=False):
        """ blockchain will be appended with new transaction and previous transaction
        Arguments 
            sender: the sender of coins
            recipient: the recipient of the coin
            amount: the amount of coins sent with the transaction
        """
        if self.public_key == None:
            return False
        trx = Transaction(sender,recipient, signature,amount)
        if Verification.verify_transaction(trx,self.get_balance):
            self.__open_transaction.append(trx)
            self.save_data()
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={'sender':sender, 'recipient':recipient, 'signature': signature, 'amount': amount})
                        if response.status_code == 400 or response.status_code == 500:
                            print('transaction declined, needs resolving')
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False




    # mining the block i.e adding thr transaction from opent pool to block
    def mine_block(self):
        if self.public_key == None:
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING',self.public_key,'' ,MINING_REWARD)
        copied_transactions = self.__open_transaction[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        # check while passing the variables(names) in the function
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        
        self.__chain.append(block)
        self.__open_transaction =[]
        self.save_data()
        return block

    def add_block(self, block):
        transactions = [Transaction(tx['sender'],tx['recipient'], tx['signature'], tx['amount']) for tx in transaction]
        proof_is_valid = Verification.valid_proof(transactions, block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        converted_block = Block(block['index'], block['previous_hash'],transactions, block['proof'], block['timestamp'])
        self.__chain.append(converted_block)
        self.save_data()
        return True

    def add_peer_node(self, node):
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        return list(self.__peer_nodes)
