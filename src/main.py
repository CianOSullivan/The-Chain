from blockchain import Blockchain
from flask import Flask, jsonify, request
from uuid import uuid4
app = Flask(__name__)
chain = Blockchain()

node_identifier = str(uuid4()).replace('-', '')

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/mine', methods=['GET'])
def mine():
    last_block = chain.get_last()
    last_proof = last_block['proof']
    proof = chain.PoW(last_proof)

    chain.new_transaction("0", node_identifier, 1)
    prev_hash = chain.hash_block(last_block)
    block = chain.new_block(proof, prev_hash)
    response = {
        'message': "New block created.",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block[proof],
        'prev_hash': block['prev_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    transaction = request.get_json(force=True)

    for val in transaction:
        if val not in ['sender', 'reciever', 'amount']:
            return "Not a full transaction", 400

    chain.new_transaction(transaction['sender'],
                          transaction['reciever'],
                          transaction['amount'])

    return {'message': 'New block to be added'}, 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': chain.chain,        # The actual blockchain
        'length': len(chain.chain),  # The number of blocks in the chain
    }
    return jsonify(response), 200


def main():
    chain.print_chain()
    chain.new_transaction("Cian", "Joan", 50.0)
    chain.print_transactions()
    chain.print_chain()
    app.run(host='localhost', port=5000)


if __name__ == "__main__":
    main()
