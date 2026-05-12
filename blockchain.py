import hashlib
import time
import json


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = {
            'index': 1,
            'timestamp': time.time(),
            'transactions': [],
            'proof': 0,
            'previous_hash': '0' * 64,
        }
        genesis['hash'] = self.hash_block(genesis)
        self.chain.append(genesis)

    def add_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

    @staticmethod
    def hash_block(block):
        block_copy = block.copy()
        block_copy.pop('hash', None)
        raw = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()

    @staticmethod
    def proof_of_work(last_proof):
        proof = 0
        prefix = '0000'
        while True:
            guess = f'{last_proof}{proof}'.encode()
            h = hashlib.sha256(guess).hexdigest()
            if h.startswith(prefix):
                break
            proof += 1
        return proof

    def mine_block(self, miner):
        last_block = self.chain[-1]
        last_proof = last_block['proof']
        proof = self.proof_of_work(last_proof)
        self.add_transaction(sender='system', recipient=miner, amount=1)
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': last_block['hash'],
        }
        block['hash'] = self.hash_block(block)
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            if curr['previous_hash'] != prev['hash']:
                return False
            curr_hash = self.hash_block(curr)
            if curr.get('hash') != curr_hash:
                return False
            guess = f'{prev["proof"]}{curr["proof"]}'.encode()
            if not hashlib.sha256(guess).hexdigest().startswith('0000'):
                return False
        return True


if __name__ == '__main__':
    bc = Blockchain()

    print('=== Mining block 2 ===')
    b2 = bc.mine_block('alice')
    print(json.dumps(b2, indent=2, default=str))
    print()

    print('=== Mining block 3 ===')
    b3 = bc.mine_block('bob')
    print(json.dumps(b3, indent=2, default=str))
    print()

    print(f'Chain valid: {bc.is_chain_valid()}')

    print('\n=== Full chain ===')
    for b in bc.chain:
        print(f'Block {b["index"]}: hash={b["hash"][:16]}... prev={b["previous_hash"][:16]}...')
