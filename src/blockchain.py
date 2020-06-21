import time
import hashlib
import json


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []

    def new_block(self, proof, previous_hash):
        """ Create a new block """
        current_block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

        self.transactions.clear()
        self.chain.append(current_block)
        return self.chain[-1]

    def new_transaction(self, sender, receiver, amount):
        """ Make a new transaction """
        self.transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        })

    def hash(block):
        """ Make a new hash for the given block """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_last(self):
        """ Get the last block """
        return self.chain[-1]
