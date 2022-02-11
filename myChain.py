import random 
import datetime
import json
import hashlib
class Blockchain(): 
 

    def __init__(self): 
        self.chain = [] 
        self.transactions = [] 
        # create Genesis block (first block of the blockchain) 
        self.create_block(proof=1, previous_hash='0')
    def create_block(self, proof, previous_hash): 
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()), 
                 'proof': proof, 
                 'previous_hash': previous_hash, 
                 'transactions': self.transactions} 
        # empty transactions 
        self.transactions = []  
        # add block to chain 
        self.chain.append(block) 
        return block 
 
    def hash(self, block): 
        encoded_block = json.dumps(block, sort_keys=True).encode() 
        return hashlib.sha1(encoded_block).hexdigest() 
    def proof_of_work(self, previous_proof): 
        new_proof = 1 
        check_proof = False 
        while check_proof is False: 
            to_be_hashed = str(new_proof**2 - previous_proof**2).encode() 
            hash_operation = hashlib.sha256(to_be_hashed).hexdigest() 
 
            # check if hash operation ends with zeros (difficulty level) 
            if hash_operation[:4] == '0000': 
                check_proof = True 
            else: 
                new_proof += 1 
        return new_proof
    def is_chain_valid(self, chain):      
        previous_block = chain[0] 
        block_index = 1 
        while block_index < len(chain):  
            current_block = chain[block_index] 
            # check 1 
            if current_block['previous_hash'] != self.hash(previous_block): 
                return False 
             
            # check 2 
            previous_proof = previous_block['proof'] 
            current_proof = current_block['proof'] 
             
            # recalculate proof of work and check it is valid 
            to_be_hashed = str(current_proof**2 - previous_proof**2).encode() 
            hash_operation = hashlib.sha256(to_be_hashed).hexdigest() 
            if hash_operation[:4] != '0000': 
                return False 
             
            # everything is good! prepare to check the next block 
            previous_block = current_block 
            block_index += 1 
         
        return True 
    def get_last_block(self): 
        return self.chain[-1]
    def add_transaction(self): 
        data = {"routers": random.randint(10, 100), 
                  "switches": random.randint(5, 15), 
                  "vlans": random.randint(100, 200)} 
        self.transactions.append(data) 
        last_block = self.get_last_block() 
        return last_block['index'] + 1  

blockchain = Blockchain()                          

def mine_block(): 
    previous_block = blockchain.get_last_block() 
    previous_proof = previous_block['proof'] 
    proof = blockchain.proof_of_work(previous_proof) 
    previous_hash = blockchain.hash(previous_block) 
    block = blockchain.create_block(proof, previous_hash) 
     
    response = {"message": "Congratulations you just mined a block!", 
                "index": block['index'], 
                "timestamp": block['timestamp'], 
                "proof": block['proof'], 
                "previous_hash": block['previous_hash'], 
                "transactions": block['transactions'] 
                }  
                
    return response
def get_chain(): 
    response = {"chain": blockchain.chain, 
                "length": len(blockchain.chain)} 
    return response 

def is_valid(): 
    is_valid = blockchain.is_chain_valid(blockchain.chain) 
    if is_valid: 
        response = {"message": "All good! Blockchain is valid."} 
    else: 
        response = {"message": "We have a problem, Blockchain is not valid"} 
    return response 

def add_transaction(): 
    index = blockchain.add_transaction() 
    response = {"message": f'This transaction will be added to Block {index}'} 
    return response