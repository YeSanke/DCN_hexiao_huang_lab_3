from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory DNS storage (you can use a file or database for persistence)
dns_records = {}

@app.route('/register', methods=['PUT'])
def register():
    # Get the hostname and IP from the body (in JSON format)
    data = request.json
    hostname = data.get('hostname')
    ip = data.get('ip')

    if not hostname or not ip:
        return jsonify({'error': 'Missing parameters'}), 400

    # Store the hostname and IP in the DNS records
    dns_records[hostname] = ip
    return jsonify({'message': 'Registration successful'}), 201

@app.route('/dns_query', methods=['GET'])
def dns_query():
    # Query for the hostname
    hostname = request.args.get('hostname')
    if not hostname:
        return jsonify({'error': 'Missing hostname parameter'}), 400

    # Check if the hostname is registered
    ip = dns_records.get(hostname)
    if not ip:
        return jsonify({'error': 'Hostname not found'}), 404

    return jsonify({'ip': ip}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=53533)
