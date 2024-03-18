import hashlib
import json
import base64

def generate_unique_key(username, user_id):
    """
    Generates a unique hash key based on user parameters.

    :param username: A string representing the username.
    :param user_id: A string representing the user ID.
    :return: A hexadecimal hash value as a string.
    """
    combined_params = f"{username}-{user_id}"
    hash_object = hashlib.sha256(combined_params.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


def verify_license_file(file_path):
    """
    Verifies the integrity of a license file stored in bytes by decoding it,
    and comparing the calculated hash of its contents against the stored hash.
    """
    license_data = None
    try:
        with open(file_path, 'rb') as file:
            encoded_license_data = file.read()
        
        # Decode the license data from Base64
        decoded_license_data = base64.b64decode(encoded_license_data)
        license_data = json.loads(decoded_license_data.decode('utf-8'))
        
        # Extract and remove the stored hash from the data
        stored_hash = license_data.pop('hash', None)
        if not stored_hash:
            return json.dumps({"License Integrity Error": "No hash found. License file corrupted"}), license_data
        
        # Recalculate the hash of the license data
        recalculated_hash = hashlib.sha256(json.dumps(license_data, indent=4).encode('utf-8')).hexdigest()
        
        # Compare the recalculated hash against the stored hash
        return json.dumps({"Status":"License integrity intact."}), license_data if stored_hash == recalculated_hash else json.dumps({"License Integrity Error":"Incorrect Hash found. License file corrupted"}), license_data
    except FileNotFoundError:
        return json.dumps({"License Integrity Error": "License file is missing. Please ensure you have a valid license."}), license_data
    except Exception as e:
        return json.dumps({"License Integrity Error":f"{e}"}), license_data

