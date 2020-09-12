from time import time
import hashlib
import json
from urllib.parse import urlparse
import requests

class Blockchain:
    def __init__(self):
        """ Make a new blockchain and create genesis block """
        self.chain = []
        self.transactions = []
        self.new_block(100, 1)  # Create the genesis block
        self.nodes = set()      # Nodes should be unique

    def new_block(self, proof, prev_hash=None):
        """ Create a new block """
        current_block = {
            'index': len(self.chain) + 1,       # The index of the current block in the chain
            'timestamp': time(),                # Stored in unix time
            'transactions': self.transactions,  # The entire list of previous transactions
            'proof': proof,                     # The proof of work
            'prev_hash': prev_hash or self.hash_block(self.get_last())  # Hash of previous block
        }

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

    def hash_block(self, block):
        """ Make a new hash for the given block """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_last(self):
        """ Get the last block in the chain """
        return self.chain[-1]

    def print_chain(self):
        """ Print each block in the chain """
        for block in self.chain:
            print(block)

    def print_transactions(self):
        """ Print the entire list of transactions"""
        for transaction in self.transactions:
            print(transaction)

    def PoW(self, last_proof):
        """
        The proof of work algorithm

        Returns the proof value once the hash ends with 4 0's
        """

        proof = 0
        hash_found = False

        # Continue working until hash ends with 4 0's
        while (hash_found is False):
            current_guess = last_proof * proof
            current_run = str(current_guess).encode()
            run_hash = hashlib.sha256(current_run).hexdigest()

            if (run_hash[:4] == "0000"):
                hash_found = True

            proof += 1

        return proof

    def reg_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        print(self.nodes)

    def validate_chain(self):
        last_block = self.chain[0]
        index = 1

        while index < len(self.chain):
            block = self.chain[index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            if block['previous_hash'] != self.hash(last_block):
                return False
            # also check if last block proof eqaills current block proof
            last_block = block
            index += 1

        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False
