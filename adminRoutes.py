from flask import Flask, jsonify

app = Flask(__name__)

# Mock data for users and products
users = [
    {'id': 1, 'name': 'John Doe', 'role': 'customer'},
    {'id': 2, 'name': 'Jane Smith', 'role': 'seller'},
    {'id': 3, 'name': 'Alice Johnson', 'role': 'customer'},
]

products = [
    {'id': 1, 'name': 'Product 1', 'price': 29.99},
    {'id': 2, 'name': 'Product 2', 'price': 39.99},
]

activity_logs = [
    {'activity': 'Login', 'count': 10},
    {'activity': 'Purchase', 'count': 5},
]

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/api/activity-logs', methods=['GET'])
def get_activity_logs():
    return jsonify(activity_logs)

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)
