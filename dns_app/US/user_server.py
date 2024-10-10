from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    # Extract query parameters
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Validate the query parameters
    if not hostname or not fs_port or not number or not as_ip or not as_port:
        return jsonify({'error': 'Missing parameters'}), 400
    
    try:
        number = int(number)  # Ensure number is an integer
    except ValueError:
        return jsonify({'error': 'Invalid number format'}), 400

    # Query the Authoritative Server to get Fibonacci Server's IP
    dns_query_url = f"http://{as_ip}:{as_port}/dns_query"
    params = {'hostname': hostname}
    response = requests.get(dns_query_url, params=params)
    
    if response.status_code != 200:
        return jsonify({'error': 'DNS query failed'}), 400

    # Get Fibonacci Server's IP from the Authoritative Server
    fibonacci_server_ip = response.json().get('ip')
    if not fibonacci_server_ip:
        return jsonify({'error': 'Fibonacci server IP not found'}), 400

    # Query the Fibonacci server for the Fibonacci number
    fibonacci_url = f"http://{fibonacci_server_ip}:{fs_port}/fibonacci"
    fibonacci_response = requests.get(fibonacci_url, params={'number': number})
    
    if fibonacci_response.status_code != 200:
        return jsonify({'error': 'Failed to get Fibonacci number'}), 400

    return jsonify(fibonacci_response.json()), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
