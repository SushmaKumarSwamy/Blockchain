from utility.hash_util import hash_string_256, hash_block


class Verification:

    # checking which hash is the 'one' based on the complexity
    @staticmethod
    def valid_proof(transactions,last_hash,proof):
        # be carefull while passing the arguments make sure hashing will cause issue for the same item (list or string matters!!str([tx....])) 
        guess = (str([tx.to_ordered_dict() for tx in transactions])+ str(last_hash)+str(proof)).encode()
        guess_hash = hash_string_256(guess)
        print(guess_hash)
        return guess_hash[0:2]=='00'


    # to check the blockchain is not tampered with some false data
    @classmethod
    def block_verify(cls,blockchain):
        for (index, block) in enumerate(blockchain):
            if index == 0 :
                continue
            if block.previous_hash != hash_block(blockchain[index-1]):
                return False
            if not cls.valid_proof(block.transactions[:-1],block.previous_hash,block.proof):
                print('proof of work is invalid')
                return False
        return True
    
        # to check whether the user has sufficient balance to send the money he intend to do 
    @staticmethod
    def verify_transaction(transaction, get_balance):
        sender_balance= get_balance()
        return sender_balance >= transaction.amount
    @classmethod
    def verify_transactions(cls,open_transaction,get_balance):
        print(open_transaction)
        return all([cls.verify_transaction(tx,get_balance) for tx in open_transaction])
