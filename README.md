# SupplyChainManagementSystem
Hands on implementation of Supply Chain Management using POET(Proof of Elapsed Time) consensus algorithm.

To run the project: python main.py
To run using an input file: type input.txt | python main.py

There are two important files in the project

main.py: This file contains the interactive command line system which gives options to the users of the SCM. These options are:
1) Register a new user: Numerical user_id along with type of the user(client/distributor) is to be entered. The user_id 0 is reserved for the   manufacturer. Only unique user_id maybe entered to register a user.
2) Add a transaction: Three types of transacations are added based on the relevant user_id: Manufacturer allocation, Distributor dispatch and Client receipt. Appropriate product_id links three transactions as one complete workflow. Issue resolution is handled by keeping a key associated with each product. The user entering incorrect key is decided as the liar, and security deposit is automatically deducted. A pre-built product_id to key dictionary is used for this: {10: "abcd", 20: "bcde", 30: "cdef", 40: "defg", 50: "efgh", 60: "fghi", 70: "ghij", 80: "hijk", 90: "ijkl", 100: "jklm"}.
3) Mine a block: PoET consensus algorithm is employed to and the node with shortest waiting time is activated first to mine the completed transactions in blocks of size 3.
4) View status: Unique product_id generates a QR code to view the status of a transaction workflow. The QR code provides status information and timestamp for all three phases of allocation, dispatch and receipt.
5) View the blockchain: All the existing blocks are displayed with each block displaying previous hash, block hash, merkle root value and transactions in the block with product_id, appropriate sender, receiver and timestamp.
6) Exit: Stops the system.

blockchain.py: This file contains the templates and utility functions for main.py. The important classes and methods are given below.

1) class Blockchain:
Important methods:
a) constructor: Initializes a blockchain with a genesis block and sets the difficulty level for mining.
b) create_genesis_block(self): Creates the first block (genesis block) with a previous hash of "0."
c) add_block(self, new_block): Adds a new block to the blockchain by mining it with the specified difficulty level.
d) is_chain_valid(self): Checks the validity of the blockchain by verifying the hash links between blocks.

2) class User
a) constructor: Initializes a user with a name, user type (e.g., 'client' or 'distributor'), security deposit, and availability status.

3) RegistrationSystem Class (RegistrationSystem):
a) constructor: : Initializes a registration system to manage users, including clients and distributors.
b) register_user(self, name, user_type, security_deposit): Registers a new user and adds them to the appropriate user list.

4)TransactionHandler Class (TransactionHandler):
a) constructor: : Initializes a transaction handler to manage transactions and conflict resolution.
b) create_transaction(self, user_id, product, amount, registration_system): Creates a new transaction based on user input and adds it to the list of pending transactions.
c) generate_qr_code(self, transaction, filename): Generates a QR code for a given transaction with relevant timestamps and product status.
d) view_status(self, product_id, blockchain): Views the status of a product in the blockchain by generating a QR code.

5) Transaction Class (Transaction):
a) constructor: Initializes a transaction with relevant details, including timestamps for manufacturer, distributor, and client actions, product status, and RSA keys for distributor and client.

6) Block Class (Block):
a) constructor: Initializes a block with a list of transactions, a previous hash, a timestamp, and a nonce for Proof of Elapsed Time (PoET) consensus.
b) calculate_merkle_root(self): Calculates the Merkle root hash of transactions in the block.
c) mine_block(self): Simulates the mining process with PoET consensus by generating random wait times for nodes and allowing the node with the shortest wait time to mine the block.
