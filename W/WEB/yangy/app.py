import datetime
import json
import hashlib
import io
from flask import Flask, jsonify, request, render_template, send_file
import matplotlib.pyplot as plt

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_blockchain(proof=1, previous_hash='0')

    def create_blockchain(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'data': []
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            current_proof = block['proof']
            hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_external_input(self, data):
        previous_block = self.get_previous_block()
        previous_proof = previous_block['proof']
        proof = self.proof_of_work(previous_proof)
        previous_hash = self.hash(previous_block)
        
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'data': data
        }
        self.chain.append(block)
        return block

app = Flask(__name__)

# Initialize four different blockchain instances
blockchain1 = Blockchain()
blockchain2 = Blockchain()
blockchain3 = Blockchain()
blockchain4 = Blockchain()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chain1/mine_block', methods=['GET'])
def mine_block_chain1():
    return mine_block(blockchain1)

@app.route('/chain1/get_chain', methods=['GET'])
def get_chain_chain1():
    return get_chain(blockchain1)

@app.route('/chain1/valid', methods=['GET'])
def valid_chain1():
    return valid(blockchain1)

@app.route('/chain1/add_input', methods=['POST'])
def add_input_chain1():
    return add_input(blockchain1)

@app.route('/chain1/chart.png')
def chart_chain1():
    return chart(blockchain1, 'chain1')

@app.route('/chain1/dashboard')
def dashboard_chain1():
    return render_template('dashboard.html', chain_name='chain1')

@app.route('/chain2/mine_block', methods=['GET'])
def mine_block_chain2():
    return mine_block(blockchain2)

@app.route('/chain2/get_chain', methods=['GET'])
def get_chain_chain2():
    return get_chain(blockchain2)

@app.route('/chain2/valid', methods=['GET'])
def valid_chain2():
    return valid(blockchain2)

@app.route('/chain2/add_input', methods=['POST'])
def add_input_chain2():
    return add_input(blockchain2)

@app.route('/chain2/chart.png')
def chart_chain2():
    return chart(blockchain2, 'chain2')

@app.route('/chain2/dashboard')
def dashboard_chain2():
    return render_template('dashboard.html', chain_name='chain2')

@app.route('/chain3/mine_block', methods=['GET'])
def mine_block_chain3():
    return mine_block(blockchain3)

@app.route('/chain3/get_chain', methods=['GET'])
def get_chain_chain3():
    return get_chain(blockchain3)

@app.route('/chain3/valid', methods=['GET'])
def valid_chain3():
    return valid(blockchain3)

@app.route('/chain3/add_input', methods=['POST'])
def add_input_chain3():
    return add_input(blockchain3)

@app.route('/chain3/chart.png')
def chart_chain3():
    return chart(blockchain3, 'chain3')

@app.route('/chain3/dashboard')
def dashboard_chain3():
    return render_template('dashboard.html', chain_name='chain3')

@app.route('/chain4/mine_block', methods=['GET'])
def mine_block_chain4():
    return mine_block(blockchain4)

@app.route('/chain4/get_chain', methods=['GET'])
def get_chain_chain4():
    return get_chain(blockchain4)

@app.route('/chain4/valid', methods=['GET'])
def valid_chain4():
    return valid(blockchain4)

@app.route('/chain4/add_input', methods=['POST'])
def add_input_chain4():
    return add_input(blockchain4)

@app.route('/chain4/chart.png')
def chart_chain4():
    return chart(blockchain4, 'chain4')

@app.route('/chain4/dashboard')
def dashboard_chain4():
    return render_template('dashboard.html', chain_name='chain4')

def mine_block(blockchain):
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_blockchain(proof, previous_hash)
    response = {
        'message': 'BLOCK MINED',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

def get_chain(blockchain):
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

def valid(blockchain):
    valid = blockchain.is_chain_valid(blockchain.chain)
    response = {'message': 'The Blockchain is valid' if valid else 'The Blockchain is not valid'}
    return jsonify(response), 200

def add_input(blockchain):
    json_input = request.get_json()
    required_fields = ['data']
    if not all(field in json_input for field in required_fields):
        return 'Invalid input', 400

    data = json_input['data']
    block = blockchain.add_external_input(data)
    response = {
        'message': 'BLOCK MINED with External Input',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'data': block['data']
    }
    return jsonify(response), 201

def chart(blockchain, chain_name):
    if chain_name == 'chain1':
        # Bar chart for chain1 to monitor the progress of the other three chains
        chain_lengths = [len(blockchain2.chain), len(blockchain3.chain), len(blockchain4.chain)]
        labels = ['Chain 2', 'Chain 3', 'Chain 4']

        plt.figure(figsize=(10, 6))
        plt.bar(labels, chain_lengths, color=['#007bff', '#ff6f61', '#28a745'])
        plt.xlabel('Chains')
        plt.ylabel('Number of Blocks')
        plt.title('Progress of Other Chains')

    else:
        # Line graph for chain2, chain3, chain4
        chain_length = len(blockchain.chain)
        indices = list(range(1, chain_length + 1))
        proofs = [block['proof'] for block in blockchain.chain]

        plt.figure(figsize=(10, 6))
        plt.plot(indices, proofs, marker='o', color='#007bff')
        plt.xlabel('Block Index')
        plt.ylabel('Proof')
        plt.title(f'Progress of {chain_name.capitalize()}')

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
