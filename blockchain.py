import hashlib
import datetime
import random
import threading
import time
import qrcode

MIN_WAIT = 2  # Minimum wait time in seconds
MAX_BACKOFF = 5  # Maximum additional random wait time in seconds

# Number of nodes participating in the PoET protocol
NUM_NODES = 5

# A list to store the wait times of each node
wait_times = [0] * NUM_NODES

# Event to signal when all nodes have committed to their wait times
commit_event = threading.Event()

# Function for each node to generate a random wait time


def generate_wait_time(node_index):
    # Generate a random additional wait time (randomBackoff)
    random_backoff = random.randint(0, MAX_BACKOFF)

    # Calculate the total wait time
    total_wait_time = MIN_WAIT + random_backoff

    # Store the wait time in the list
    wait_times[node_index] = total_wait_time

    # Signal that this node has committed to its wait time
    commit_event.set()


class Transaction:
    def __init__(self, product_id, manufacturer, distributor,distributor_key, client,client_key, amount, timestamp_m, timestamp_d, timestamp_c):
        self.manufacturer = manufacturer
        self.product_id = product_id
        self.distributor = distributor
        self.distributor_key = distributor_key  
        self.client = client
        self.client_key = client_key
        self.amount = amount
        self.timestamp_m = timestamp_m
        self.timestamp_d = timestamp_d
        self.timestamp_c = timestamp_c
        self.product_status = False


    def calculate_hash(self):
        # Calculate the hash of the transaction
        transaction_data = (
            str(self.product_id)
            + str(self.distributor)
            + str(self.client)
            + str(self.amount)
            + str(self.timestamp_m)
            + str(self.timestamp_d)
            + str(self.timestamp_c)
            + str(self.product_id)  # Include the product ID in the hash
        )
        return hashlib.sha256(transaction_data.encode()).hexdigest()


class Block:
    def __init__(self, previous_hash):
        self.transactions = []
        self.previous_hash = previous_hash
        self.timestamp = datetime.datetime.now()
        self.merkle_root = 0

    def calculate_merkle_root(self):
        # Calculate the Merkle root of transactions
        if not self.transactions:
            return ""

        # Create a list of transaction hashes
        transaction_hashes = [tx.calculate_hash() for tx in self.transactions]

        # Calculate the Merkle root
        while len(transaction_hashes) > 1:
            new_hashes = []
            for i in range(0, len(transaction_hashes), 2):
                if i + 1 < len(transaction_hashes):
                    combined = transaction_hashes[i] + \
                        transaction_hashes[i + 1]
                else:
                    combined = transaction_hashes[i]+transaction_hashes[i]
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_hashes.append(new_hash)
            transaction_hashes = new_hashes

        return transaction_hashes[0]

    def mine_block(self):
        # Create and start threads for each node
        threads = []
        for node_index in range(NUM_NODES):
            thread = threading.Thread(
                target=generate_wait_time, args=(node_index,))
            thread.start()
            threads.append(thread)

        # Wait for all nodes to commit to their wait times
        commit_event.wait()

        # Find the shortest wait time among all nodes
        for i in range(len(wait_times)):
            print({i, wait_times[i]})
        shortest_wait_time = min(wait_times)
        time.sleep(shortest_wait_time)
        # Simulate work for each node based on their wait time
        node_index = wait_times.index(shortest_wait_time)
        print(
            f"Node {node_index + 1} with the shortest wait time of {shortest_wait_time} seconds is activated and has added the block.")

    def calculate_hash(self):
        # Calculate the hash of the block
        block_data = (
            str(self.timestamp) + self.calculate_merkle_root() +
            str(self.previous_hash)
        )
        return hashlib.sha256(block_data.encode()).hexdigest()

    


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Create the first block in the chain (genesis block)
        return Block("0")  # Previous hash is "0"

    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].calculate_hash()
        new_block.mine_block()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the previous hash matches the actual previous block's hash
            if current_block.previous_hash != previous_block.calculate_hash():
                return False

        return True


class User:
    def __init__(self, name, user_type, security_deposit,  user_availability=True):
        self.name = name
        self.user_type = user_type  # 'client' or 'distributor'
        self.user_availability = user_availability
        self.security_deposit = security_deposit


class RegistrationSystem:
    def __init__(self):
        self.clientuserIdList = set()
        self.distuserIdList = set()
        self.clients = [] 
        self.distributors = []
        self.dist_map = {}

    def register_user(self, name, user_type, security_deposit):
        # Create a new user and add to the list of registered users
        # user types can be :- client, manufacturer or distrwibutor
        user = User(name, user_type, security_deposit, user_availability=True)

        if (user_type == 1):
            self.distributors.append(user)
            self.distuserIdList.add(user.name)
            self.dist_map[user.name]=user
        else:
            self.clients.append(user)
            self.clientuserIdList.add(user.name)
        return user


class TransactionHandler:
    def __init__(self):
        self.pending_transactions = []  # List to store pending transactions
        self.product_to_key_map = {10: "abcd", 20: "bcde", 30: "cdef", 40: "defg", 50: "efgh", 60: "fghi", 70: "ghij", 80: "hijk", 90: "ijkl", 100: "jklm"}
        self.product_to_block_map = {}
        self.product_to_transaction_map = {}
    
    def conflict_resolution(self,product_id, transaction, registration_system):
        correct_key = self.product_to_key_map[product_id]
        distributor_key = transaction.distributor_key
        client_key = transaction.client_key
        
        #print(correct_key, distributor_key, client_key)
        if(distributor_key != correct_key):
            dist_id = transaction.distributor
            for i in registration_system.distributors:
                if(dist_id == i.name):
                    print("Distributor lying\nAvailable balance: ", i.security_deposit)
                    i.security_deposit -= 100
                    print("New balance : " , i.security_deposit)
                    break
        elif(client_key != correct_key):
            client_id = transaction.client
            print("Client id is: ", client_id)
            for i in registration_system.clients:
                if(client_id == i.name):
                    print("Client lying\nAvailable balance: ", i.security_deposit)
                    i.security_deposit -= 100
                    print("New balance : " , i.security_deposit)
                    break
        else:
            print("No conflict!")
            return
            

    def create_transaction(self, user_id, product, amount, registration_system):
        if (user_id == 0):
            # manufacturer trans
            dist_id = -1
            timestamp = datetime.datetime.now()

            for i in range(len(registration_system.distributors)):
                if (registration_system.distributors[i].user_availability == True):
                    dist_id = registration_system.distributors[i].name
                    registration_system.distributors[i].user_availability = False
                    break
            if (dist_id == -1):
                print("No distributors available")
                return
            print("\nDistributor assigned: ", dist_id)
            transaction = Transaction(
                product, 0, dist_id,None, None,None, amount, timestamp, None, None)
            self.pending_transactions.append(transaction)
            self.product_to_transaction_map[product] = transaction
            print("Transaction Successful\n")
            print("\nDistributor assigned: ", dist_id)
        elif (user_id in registration_system.distuserIdList):
            if (self.product_to_transaction_map[product].distributor != user_id):
                print("\nProduct assigned to distributor : ", self.product_to_transaction_map[product].distributor)
                return
            client_id = int(input("Enter client ID: "))
            if (client_id not in registration_system.clientuserIdList):
                print("Client not registered")
                return
            distributor_key = input("Enter correct product key: ")
            

            for i in self.pending_transactions:
                if (i.product_id == product):
                    i.client = client_id
                    i.distributor_key = distributor_key
                    i.timestamp_d = datetime.datetime.now()
                    print("Transaction Successful\n")
                    return

            #print("Invalid Transaction")

        elif (user_id in registration_system.clientuserIdList):
            if(self.product_to_transaction_map[product].timestamp_d == None):
                print("Invalid transaction\n")
                return
            if(self.product_to_transaction_map[product].client != user_id):
                print("You are not the intended receipent for product ", product)
                return
            client_say = int(input("If product received enter 1 else 0: "))
            
            client_key = input("Enter correct product key: ")
            for i in self.pending_transactions:
                if (i.product_id == product):
                    i.client_key = client_key
                    i.timestamp_c = datetime.datetime.now()
                    if(client_say == 0):
                        print("\nConflict detected\n")
                        self.conflict_resolution(product, i, registration_system)
                    i.product_status = True
                    print("Transaction Successful\n")
                    registration_system.dist_map[i.distributor].user_availability=True
                    
                    return

            #print("Invalid Transaction\n")

        else:
            # invalid userid
            print("Invalid user ID\n")
            return

        
    def generate_qr_code(self, transaction, filename):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # data = f"{transaction.timestamp_m} :: {transaction.timestamp_d} :: {transaction.timestamp_c}\n {transaction.product_status}"
        data=f"Distributor assigned at ::{transaction.timestamp_m}\n"
        if(not transaction.timestamp_d):
            data += "Product not dispatched\n"
        else:
            data += f"Product dispatched at ::{transaction.timestamp_d}\n"
        if(not transaction.timestamp_c):
            data += "Product not received\n"
        else:
            data += f"Product received at ::{transaction.timestamp_c}\n"
        print(data)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        img.save(filename)

    def view_status(self, product_id, blockchain):
        for block in blockchain.chain:
            for transaction in block.transactions:
                if (transaction.product_id == product_id):
                    self.generate_qr_code(transaction, f"qr_{product_id}.png")
                    return
        for tr in self.pending_transactions:
            if (tr.product_id == product_id):
                self.generate_qr_code(tr, f"qr_{product_id}.png")
                return
