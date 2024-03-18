import functools
from datetime import datetime
import json
from .helpers.security import generate_unique_key, verify_license_file
import re


def check_license_premium(func):
    """
    Decorator that checks for a valid license before allowing a function to execute.
    """
    @functools.wraps(func)
    def wrapper_check_license_premium(*args, **kwargs):
        license_file_path = "D:/OS int tool/license.lic"  # Update path to actual license file
        integrity, license_data = verify_license_file(license_file_path)
        if re.search("License integrity intact.", integrity):
            # Example user parameters
            username = "exampleUsername" # get username from current session
            user_id = "12345" # get user ID from current session
            expected_unique_key = generate_unique_key(username, user_id)

            try:
                if expected_unique_key != license_data["uniqueKey"]:
                    return json.dumps({"error": "Invalid license key. Please check your license file."})
                
                # Get license type and expiry date
                license_type = None
                expiration_date = None

                license_type = license_data["type"]
                expiration_date_str = license_data["expiration"]
                expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d")

                if not license_type == "Premium":
                    return json.dumps({"error": f"Invalid license type. Please ensure your license is valid."})
                    
                if expiration_date and expiration_date < datetime.now():
                    return json.dumps({"error": "License has expired. Please renew your license."})
                    
            except Exception as e:
                return json.dumps({"error": f"An error occurred while processing the license file: {e}"})
        else:
            return integrity
        return func(*args, **kwargs)
    return wrapper_check_license_premium


def check_license_standard(func):
    """
    Decorator that checks for a valid license before allowing a function to execute.
    """
    @functools.wraps(func)
    def wrapper_check_license_standard(*args, **kwargs):
        license_file_path = "D:/OS int tool/license.lic"  # Update path to actual license file
        integrity, license_data, *x = verify_license_file(license_file_path)
        if re.search("License integrity intact.", integrity):
        # Example user parameters
            username = "exampleUsername" # get username from current session
            user_id = "12345" # get user ID from current session
            expected_unique_key = generate_unique_key(username, user_id)

            try:
                if expected_unique_key != license_data["uniqueKey"]:
                    return json.dumps({"error": "Invalid license key. Please check your license file."})
                
                # Get license type and expiry date
                license_type = None
                expiration_date = None

                license_type = license_data["type"]
                expiration_date_str = license_data["expiration"]
                expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d")

                if not license_type == "Standard":
                    return json.dumps({"error": f"Invalid license type. Please ensure your license is valid."})
                    
                if expiration_date and expiration_date < datetime.now():
                    return json.dumps({"error": "License has expired. Please renew your license."})
                    
            except Exception as e:
                return json.dumps({"error": f"An error occurred while processing the license file: {e}"})
        
        else:
            return integrity

        return func(*args, **kwargs)
    return wrapper_check_license_standard


