<div align="center">
	<img width="256" src="assets/logo.png" alt="The Chain logo">
</div>

# The-Chain
Blockchain implementation written in Python.

Live demo available at: [chain.cianosullivan.me](https://chain.cianosullivan.me). Spin up your own instance of The-Chain and add the node on the site to contribute transactions to the network!
# Running the blockchain
To run the blockchain:

```
git clone https://github.com/CianOSullivan/The-Chain
cd The-Chain
python3 src/main.py
```

This will start the flask server and initialise the blockchain with the genesis node.  
To access the blockchain, navigate to https://localhost:5000 and use the 'transaction' and 'mine' tabs to interact with it.

# Usage

```
usage: main.py [-h] [--host HOST] [--port PORT]

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  the desired hostname of the blockchain server
  --port PORT  the desired port number of the blockchain server
```

# Screenshots

![Home](assets/home.png)

![Transaction](assets/transaction.png)

![Mine](assets/mine.png)

![Node](assets/node.png)
