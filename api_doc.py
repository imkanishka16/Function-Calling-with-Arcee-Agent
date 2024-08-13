from flask import Flask, jsonify, request
from data_store import list, offers,register,new_packages
from data_store import register
import numpy as np
import data_store
app = Flask(__name__)

def is_nic_registered(nic_number, register_data):
    for person in register_data["registered"]:
        if person["NIC"] == nic_number:
            return True
    return False

@app.route('/register_status', methods=['POST'])
def check_register_nic():
    """
    Check if a NIC number is registered.

    This endpoint verifies if a provided NIC number is already registered.
    If registered, it returns the associated name and connection details.
    If not registered, it prompts for a NIC image in .png or .jpg format.

    Form Data:
        nic_number (str): The NIC number to check.

    Responses:
        200 OK: NIC number is registered, returns name and connections.
        201 Created: NIC number is not registered, requests NIC image.
        400 Bad Request: NIC number not provided.
    """
    data = request.form  # Accessing form data correctly
    nic_number = data.get('nic_number')
    # image_file = request.files.get('image_file')
    
    if nic_number is None:
        return jsonify({'error': 'NIC number is required'}), 400
    
    if is_nic_registered(nic_number, register):
        # Fetch and return existing connections
        for person in register["registered"]:
            if person["NIC"] == nic_number:
                return jsonify({
                    'message': f'The NIC {nic_number} is already registered under the name {person["name"]}.',
                    'connections': {
                        'mbb': person["mbb"],
                        'hbb': person["hbb"],
                        'dtv': person["dtv"]
                    }
                }), 200
    else:
        return jsonify({'message': 'You need to give NIC image as .png or .jpg format to continue'}), 201
    
    
@app.route('/list',methods = ['GET'])
def get_menu():
    """
    Retrieves the list data.
    Returns:
        A tuple containing the list data as JSON and the HTTP status code.
    """
    return jsonify(list), 200

@app.route('/special_offers', methods=['GET'])
def get_special_offer():
    offers_list = data_store.offers["offers"]
    formatted_offers = ""
    for offer in offers_list:
        formatted_offers += f"description = {offer['description']}\n"
        formatted_offers += f"url = {offer['url']}\n\n"
    return formatted_offers, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/new_package', methods = ['GET'])
def get_new_packages():
    """
    Retrieves the special offer
    Return:
        A tuple containing the special offers data as JSON and the HTTP status code.
    """
    return jsonify(new_packages), 200

if __name__ == '__main__':
    app.run(debug = True)