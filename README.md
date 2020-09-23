<div align="center">
	<img width="256" src="assets/logo.png" alt="The Chain logo">
</div>

# The-Chain
Blockchain implementation written in Python.

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

