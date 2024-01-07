from blockchain import Block, Blockchain, RegistrationSystem, TransactionHandler, User

# Create a blockchain
blockchain = Blockchain()
# Create a transaction handler
transaction_handler = TransactionHandler()
# Create users
registration_system = RegistrationSystem()

def displayAll():
    print("The distributors in the blockchain are :")
    for dist in registration_system.distuserIdList:
        print(dist)
    print()
    print("The clients in the blockchain are :")
    for client in registration_system.clientuserIdList:
        print(client)

password="1234"

def addProductKey():
    pwd=input("Enter password: ")
    if(pwd==password):
        product_id=int(input("Enter product id: "))
        if(product_id in transaction_handler.product_to_key_map):
            print("Product already exists")
            return
        product_key=input("Enter product key: ")
        transaction_handler.product_to_key_map[product_id]=product_key
        print("Product added successfully!\n")
    else:
        print("Unauthorized Access\n")
        
     
def display_blockchain_status():
    print("\nBlockchain Status:")
    for block in blockchain.chain:
        print("Block Previous Hash: ", block.previous_hash)
        print("Block Hash: ", block.calculate_hash())
        print("Merkle root value", block.merkle_root)
        print("Number of transactions: ", len(block.transactions))
        for tx in block.transactions:
            print("Product ID: ", tx.product_id) 
            print("From: "+str(tx.manufacturer)+" To: "+str(tx.distributor)+" Amount: "+str(tx.amount)+ " Timestamp: "+ str(tx.timestamp_m))
            print("From: "+str(tx.distributor)+" To: "+str(tx.client)+" Amount: "+str(tx.amount)+ " Timestamp: "+ str(tx.timestamp_d))
            print("From: "+str(tx.client)+" To: "+str(tx.distributor)+" Amount: "+str(tx.amount)+ " Timestamp: "+ str(tx.timestamp_c))
        print()


numberOfTransactions = 0
numberofBlocks = 0

while (True):

    user_input = int(input(
        "Enter 1 to Register a new user\nEnter 2 to Add a transaction\nEnter 3 to mine a block\nEnter 4 to view status\nEnter 5 to view the blockchain\nEnter 6 to get all distributors and clients\nEnter 7 to display products\nEnter 8 to add a New Product\nEnter 9 to exit\n"))

    if (user_input == 1):
        user_id = int(input("\nEnter user id: "))
        if (user_id in registration_system.clientuserIdList | registration_system.distuserIdList):
            print("User already registered")
            continue
        user_type = int(
            input("Enter 1 for adding a distributor\nEnter 2 for adding a client\n"))
        security_deposit = int(input("Enter security deposit amount:\n"))

       
        if(user_type==1):
            print("Success! Distributor registered\n")
            registration_system.register_user(
            user_id, user_type, security_deposit)
        elif(user_type==2):
            print("Success! User registered\n")
            registration_system.register_user(
            user_id, user_type, security_deposit)
        else:
            print("Please Enter either 1 or 2")
            continue

    elif (user_input == 2):  # Transaction add
        user_id = int(input("Enter user id: "))
        product = int(input("Enter product id: "))
        notPresent = product not in transaction_handler.product_to_key_map
        notValid = user_id != 0 and product not in transaction_handler.product_to_transaction_map
        if notPresent or notValid:
            print("\nInvalid product ID\n")
            continue
        elif (not notPresent and product in transaction_handler.product_to_transaction_map and transaction_handler.product_to_transaction_map[product].product_status):
            print("\nInvalid product ID\n")
            continue
        
        amount = float(input("Enter Amount: \n"))

        transaction_handler.create_transaction(
            user_id, product, amount, registration_system)

    elif (user_input == 3):
        verified_transactions = [i for i in transaction_handler.pending_transactions if i.product_status]
        for i in transaction_handler.pending_transactions:
            if(i.product_status):
                transaction_handler.pending_transactions.remove(i)
        k = 3
        for i in range(len(verified_transactions) // k):
            new_block = Block(blockchain.chain[-1].calculate_hash())
            new_block.transactions = verified_transactions[k*i:k*i+k].copy()
            new_block.merkle_root = new_block.calculate_merkle_root()
            for i in verified_transactions:
                transaction_handler.product_to_block_map[i.product_id] = new_block
            blockchain.add_block(new_block)
            numberofBlocks += 1
        transaction_handler.pending_transactions += verified_transactions[k*(len(verified_transactions)//k):]


    elif (user_input == 4):
        product_id = int(input("Enter product id to be verified\n"))
        if(product_id not in transaction_handler.product_to_key_map):
            print("Enter valid product ID")
            continue
        transaction_handler.view_status(product_id, blockchain)
        
    elif(user_input==5):
        display_blockchain_status()
        
    elif(user_input==6):
        displayAll()

    elif(user_input==7):
            print(transaction_handler.product_to_key_map)
    elif(user_input==8):
        addProductKey()
    else:
        print("Exiting")
        break