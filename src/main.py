from blockchain import Blockchain
from flask import Flask, jsonify

app = Flask(__name__)
chain = Blockchain()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new Block"


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return "We'll add a new transaction"


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
