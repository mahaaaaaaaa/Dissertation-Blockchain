# Dissertation-Blockchain

This is a simple proof-of-stake blockchain created for the purpose of understanding blockchain technologies and creating an artifact for my dissertation.

## Usage

RUN 'py -m pip install -r requirements.txt' on first run, this will install the required libraries for the program.
Then run python main.py localhost '10000 5000 keys/genesisPrivateKey.pem', this will create a local node that will act as the discovery route for other nodes.
Subsequent nodes can be created by running 'python main.py IP PORT APIPORT', using a keypair is optional.
