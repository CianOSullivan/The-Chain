from blockchain import Blockchain
from flask import Flask, jsonify, request, render_template, Markup
from uuid import uuid4
import argparse

NODE_ID = str(uuid4()).replace('-', '')  # The universally unique id of this node
app = Flask(__name__)
chain = Blockchain()


@app.route('/')
def index_page():
    """ Display the index page for the flask server """
    chain.reg_node("http://localhost:5000")
    return render_template("index.html")


@app.route('/transaction')
def transaction_page():
    """ Return the transaction form """
    return render_template("transaction.html")


@app.route('/register')
def registration_page():
    """ Return the transaction form """
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def new_node_form():
    """ Add transaction to the chain if it is valid """
    node_name = request.form['node']

    # If node_name doesnt start with http:// then it is not valid and must be refused


    if (node_name):
        registration = Markup('<p class="subtitle has-text-success">Node registered. \n </p>')
        chain.reg_node(node_name)
    else:
        # Send error message on failed transaction
        registration = Markup('<p class="subtitle has-text-danger">Node registration failed.</p>')

    return render_template("register.html", registration=registration)


@app.route('/transaction', methods=['POST'])
def transaction_form():
    """ Add transaction to the chain if it is valid """
    sender = request.form['sender']
    reciever = request.form['reciever']
    amount = request.form['amount']

    # If valid transaction, update message and make transaction
    if (sender and reciever and amount):
        transaction = Markup('<p class="subtitle has-text-success">Transaction executed: \n' +
                             sender + ' => ' + reciever + ': ' + amount + '</p>')
        chain.new_transaction(sender, reciever, amount)
    else:
        # Send error message on failed transaction
        transaction = Markup('<p class="subtitle has-text-danger">Transaction Failed: ' +
                             'Must complete form</p>')

    return render_template("transaction.html", transaction=transaction)


@app.route('/mine', methods=['GET'])
def mine():
    """ Create a new block """
    last_block = chain.get_last()
    last_proof = last_block['proof']  # The PoW of the last block
    proof = chain.PoW(last_proof)
    chain.new_transaction("0", NODE_ID, 1)
    block = chain.new_block(proof, chain.hash_block(last_block))

    response = {
        'message': "Block " + str(block['index']) + " created.",  # The index of the current block
        'Number of transactions': len(block['transactions']),     # The num of transactions in list
        'transactions': block['transactions'],                    # The list of transactions
        'proof': block['proof'],                                  # The proof of work
        'prev_hash': block['prev_hash'],                          # The hash value of prev block
    }

    return render_template("mine.html", response=response)


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """ Add a new transaction to the list using HTTP POST method """
    transaction = request.get_json(force=True)

    # Check it is a full transaction
    for val in transaction:
        if val not in ['sender', 'reciever', 'amount']:
            return "Not a full transaction", 400

    # Add the new transaction to the list
    chain.new_transaction(transaction['sender'],
                          transaction['reciever'],
                          transaction['amount'])

    return {'message': 'New block to be added'}, 201  # Return the success message and code


@app.route('/chain', methods=['GET'])
def full_chain():
    """ Return the entire blockchain in json format """
    response = {
        'chain': chain.chain,        # The actual blockchain
        'length': len(chain.chain),  # The number of blocks in the chain
    }
    return jsonify(response), 200  # Return the blockchain and a success code


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        chain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(chain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = chain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': chain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': chain.chain
        }

    return jsonify(response), 200


def main(host_name, port_num):
    app.run(threaded=True, host=host_name, port=port_num)  # Start the flask server


if __name__ == "__main__":
    # Initialise default arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default="localhost",
                        help="the desired hostname of the blockchain server")
    parser.add_argument('--port', type=int, default=5000,
                        help="the desired port number of the blockchain server")
    args = parser.parse_args()

    main(args.host, args.port)
