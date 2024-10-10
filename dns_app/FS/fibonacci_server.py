from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Calculate Fibonacci number
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    try:
        number = int(request.args.get('number'))
    except ValueError:
        return jsonify({'error': 'Invalid number'}), 400

    fib_number = fibonacci(number)
    return jsonify({'Fibonacci number': fib_number}), 200

@app.route('/register', methods=['PUT'])
def register():
    # Receive the hostname, IP, as_ip, and as_port from the body (in JSON format)
    data = request.json
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not hostname or not ip or not as_ip or not as_port:
        return jsonify({'error': 'Missing parameters'}), 400

    # Register with Authoritative Server
    register_url = f"http://{as_ip}:{as_port}/register"
    registration_data = {
        'hostname': hostname,
        'ip': ip
    }
    response = requests.put(register_url, json=registration_data)

    if response.status_code != 201:
        return jsonify({'error': 'Registration with Authoritative Server failed'}), 400

    return jsonify({'message': 'Registration successful'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
