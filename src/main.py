from blockchain import Blockchain
from flask import Flask, jsonify, request, render_template, Markup
from uuid import uuid4

app = Flask(__name__)
chain = Blockchain()
NODE_ID = str(uuid4()).replace('-', '')  # The universally unique id of this node


@app.route('/')
def index_page():
    """ Display the index page for the flask server """
    return render_template("index.html")


@app.route('/transaction')
def transaction_page():
    """ Return the transaction form """
    return render_template("transaction.html")


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


def main():
    app.run(host='localhost', port=5000)  # Start the flask server


if __name__ == "__main__":
    main()
