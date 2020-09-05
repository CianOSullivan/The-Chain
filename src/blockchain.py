from time import time
import hashlib
import json


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.new_block(100, 1)

    def new_block(self, proof, previous_hash=None):
        """ Create a new block """
        current_block = {
            'index': len(self.chain) + 1,       # The index of the current block in the chain
            'timestamp': time(),                # Stored in unix time
            'transactions': self.transactions,  # The entire list of previous transactions
            'proof': proof,
            'previous_hash': previous_hash or self.hash_block(self.get_last())
        }

        self.transactions.clear()
        self.chain.append(current_block)
        return current_block

    def new_transaction(self, sender, receiver, amount):
        """ Make a new transaction """
        self.transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        })

        return self.get_last()['index'] + 1

    def hash_block(block):
        """ Make a new hash for the given block """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_last(self):
        """ Get the last block """
        return self.chain[-1]

    def print_chain(self):
        for block in self.chain:
            print(block)

    def print_transactions(self):
        for transaction in self.transactions:
            print(transaction)

    def pow(self, last_proof):
        proof = 0
        while (self.do_work() is False):
            proof += 1
        return proof

    def do_work(last_proof, proof):
        current_guess = last_proof * proof
        current_run = str(current_guess).encode()
        run_hash = hashlib.sha256(current_run).hexdigest()
        if (run_hash[:4] == "0000"):
            return True
        return False
