from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the path to your text file database
DATABASE_FILE = 'products.txt'

# Helper function to read data from the text file
def read_data():
    try:
        with open(DATABASE_FILE, 'r') as file:
            data = file.readlines()
        return [line.strip().split(',') for line in data]
    except FileNotFoundError:
        return []

# Helper function to write data to the text file
def write_data(data):
    with open(DATABASE_FILE, 'w') as file:
        for line in data:
            file.write(','.join(map(str, line)) + '\n')

@app.route('/add', methods=['POST'])
def add_product():
    data = read_data()
    product = request.json

    if not data or data[0][0] == 'id':
        # If the file is empty or contains only the header, start fresh
        data = []

    data.append([product['id'], product['name'], product['price'], product['quantity']])
    write_data(data)
    return jsonify({"message": "Product added successfully"})

@app.route('/update', methods=['PUT'])
def update_product():
    data = read_data()
    product = request.json
    for i, existing_product in enumerate(data):
        if existing_product[0] == product['id']:
            data[i] = [product['id'], product['name'], product['price'], product['quantity']]
            write_data(data)
            return jsonify({"message": "Product updated successfully"})
    return jsonify({"error": "Product not found"})

@app.route('/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    data = read_data()
    for i, product in enumerate(data):
        if product[0] == product_id:
            del data[i]
            write_data(data)
            return jsonify({"message": "Product deleted successfully"})
    return jsonify({"error": "Product not found"})

@app.route('/listproducts', methods=['GET'])
def list_products():
    data = read_data()
    return jsonify({"products": data})

@app.route('/getquantity/<product_id>', methods=['GET'])
def get_quantity(product_id):
    data = read_data()
    for product in data:
        if product[0] == product_id:
            return jsonify({"quantity": int(product[3])})
    return jsonify({"error": "Product not found"})

@app.route('/getprice/<product_id>', methods=['GET'])
def get_price(product_id):
    data = read_data()
    for product in data:
        if product[0] == product_id:
            return jsonify({"price": float(product[2])})
    return jsonify({"error": "Product not found"})

if __name__ == '__main__':
    app.run(debug=True)
