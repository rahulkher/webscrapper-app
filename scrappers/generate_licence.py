from .helpers.security import generate_unique_key
from .helpers.security import calculate_hash
from .helpers.security import verify_integrity

import hashlib
import json
import base64

def create_license_file(license_data, file_path):
    """
    Creates a license file with given data, calculates its SHA-256 hash,
    and stores both in the file in JSON format.
    """
    # Convert license data to JSON and calculate its SHA-256 hash
    license_json = json.dumps(license_data, indent=4)
    sha256_hash = hashlib.sha256(license_json.encode('utf-8')).hexdigest()
    
    # Append the hash to the license data
    license_data['hash'] = sha256_hash
    
    # Convert updated license data to JSON
    updated_license_json = json.dumps(license_data, indent=4)
    
    # Encode the entire license data with hash in Base64
    encoded_license_data = base64.b64encode(updated_license_json.encode('utf-8'))
    
    # Write the encoded license data (in bytes) to the file
    with open(file_path, 'wb') as file:
        file.write(encoded_license_data)

# Example license data
license_data = {
    "type": "Standard",
    "expiration": "2024-12-31",
    "uniqueKey": str(generate_unique_key(username="exampleUsername", user_id="12345")).strip()
}

file_path = 'D:\OS int tool\license.lic'
create_license_file(license_data, file_path)
