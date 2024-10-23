from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

client_weights = []

@app.route('/')
def index():
    return "Federated Learning Service is running"


@app.route('/federatedlearning/train', methods=['POST'])
def receive_weights():
    data = request.json
    weights = data.get('weights')  
    if weights:
        client_weights.append(weights) 
        return jsonify({"message": "Weights received", "status": "success"}), 200
    else:
        return jsonify({"message": "No weights provided", "status": "failure"}), 400


@app.route('/federatedlearning/aggregate', methods=['GET'])
def aggregate_weights():
    if not client_weights:
        return jsonify({"message": "No client weights to aggregate", "status": "failure"}), 400
    
    
    aggregated_weights = np.mean(client_weights, axis=0)
    
   
    client_weights.clear()
    
    return jsonify({"global_weights": aggregated_weights.tolist(), "status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9556)
