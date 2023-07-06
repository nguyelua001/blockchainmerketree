import hashlib


class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.merkle_root = self.build_merkle_tree()

    def build_merkle_tree(self):
        # Check if the number of transactions is a power of 2
        if len(self.transactions) % 2 != 0:
            self.transactions.append(self.transactions[-1])

        # Build the initial list of transaction hashes
        transaction_hashes = [self.hash_transaction(tx) for tx in self.transactions]

        # Continue hashing pairs until we reach the root
        while len(transaction_hashes) > 1:
            transaction_hashes = self.compute_next_level(transaction_hashes)

        return transaction_hashes[0]

    def compute_next_level(self, transaction_hashes):
        next_level = []

        for i in range(0, len(transaction_hashes), 2):
            combined_hash = transaction_hashes[i] + transaction_hashes[i + 1]
            next_level.append(self.hash_transaction(combined_hash))

        return next_level

    def hash_transaction(self, transaction):
        return hashlib.sha256(transaction.encode()).hexdigest()

    def visualize_merkle_tree(self, level_hashes):
        if len(level_hashes) == 1:
            print(f"??? {level_hashes[0]}")
            return

        num_hashes = len(level_hashes)
        next_level_hashes = self.compute_next_level(level_hashes)

        for i in range(num_hashes):
            if i == 0:
                print("???", end=" ")
            elif i == num_hashes - 1:
                print("???", end=" ")
            else:
                print("?  ", end=" ")

            print(level_hashes[i])

        self.visualize_merkle_tree(next_level_hashes)


class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_tree = MerkleTree(transactions)

    def hash_block(self):
        header = str(self.previous_hash) + self.merkle_tree.merkle_root
        return hashlib.sha256(header.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        # Create the genesis block
        genesis_block = Block([], "0")
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        previous_hash = self.chain[-1].hash_block()
        new_block = Block(transactions, previous_hash)
        self.chain.append(new_block)

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_block(self, miner_address):
        if not self.pending_transactions:
            return None

        # Include a reward transaction for the miner
        reward_transaction = f"Reward: {miner_address} received 1 BTC"
        self.pending_transactions.append(reward_transaction)

        self.add_block(self.pending_transactions)
        self.pending_transactions = []

        return self.chain[-1]

    def get_chain_length(self):
        return len(self.chain)


# Example usage:
if __name__ == "__main__":
    blockchain = Blockchain()

    # Add transactions to the pending transaction pool
    blockchain.add_transaction("Alice sends 1 BTC to Bob")
    blockchain.add_transaction("Bob sends 0.5 BTC to Charlie")

    # Mine a new block with the pending transactions
    mined_block = blockchain.mine_block("Miner1")
    #print(f"Mined block: {mined_block.hash_block()}

