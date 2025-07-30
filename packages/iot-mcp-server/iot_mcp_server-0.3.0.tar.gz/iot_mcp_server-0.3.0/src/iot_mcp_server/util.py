import os
import time
import hashlib
import urllib.parse
import requests
import jwt  # Add this import at the top

def get_access_token():
    """Check if current token exists and is valid (not expired or expiring within 1 hour)"""
    access_token = os.environ.get('ACCESS_TOKEN')
    
    if access_token:
        try:
            # Decode token without verification to check expiration
            decoded = jwt.decode(access_token, options={"verify_signature": False})
            exp_time = decoded.get('exp')
            
            if exp_time and (exp_time - time.time() > 3600):  # More than 1 hour remaining
                return access_token
        except jwt.DecodeError:
            pass  # Token is invalid, will get new one
    
    # If we get here, either no token or it's expired/expiring soon
    access_token = _get_access_token()
    if access_token:
        os.environ['ACCESS_TOKEN'] = access_token
        return access_token
    
    print("Error: Failed to get access token")
    return None

def _get_access_token():
    access_key = os.environ.get('ACCESS_KEY')
    access_secret = os.environ.get('ACCESS_SECRET')
    
    if not access_key or not access_secret:
        return "Error: Missing ACCESS_KEY or ACCESS_SECRET"
    
    # Generate token request parameters
    timestamp = str(int(time.time() * 1000))
    username_params = {
        'ver': '1',
        'auth_mode': 'accessKey',
        'sign_method': 'sha256',
        'access_key': access_key,
        'timestamp': timestamp
    }
    username_plain = '&'.join(f"{k}={v}" for k, v in username_params.items())
    username = urllib.parse.quote(username_plain, safe="!'()*-._~")
    
    # Generate password hash
    password_plain = f"{username_plain}{access_secret}"
    password = hashlib.sha256(password_plain.encode('utf-8')).hexdigest()

    base_url = os.environ.get('BASE_URL')
    url = f"{base_url}/v2/quecauth/accessKeyAuthrize/accessKeyLogin?grant_type=password&username={username}&password={password}"

    # Make API request to get token
    try:
        response = requests.get(url, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get('access_token')
        print(f"Token: {access_token}")
        return access_token
    except Exception as e:
        print(f"API Error: {str(e)}")
        return "Error: Making the accessKeyLogin request error"

def list_products():
    base_url = os.environ.get('BASE_URL')
    url = f"{base_url}/v2/quecproductmgr/r3/openapi/products"
    try:
        response = requests.get(url, headers={
            "Content-Type": "application/json",
            "Authorization": get_access_token()
        })
        response.raise_for_status()
        content = response.json()
        return content["data"]
    except Exception as e:
        print(f"API Error: {str(e)}")
        return "Error: List products error"

def get_product_tsl_json(product_key):
    base_url = os.environ.get('BASE_URL')
    url = f"{base_url}/v2/quectsl/openapi/product/export/tslFile?productKey={product_key}"
    try:
        response = requests.get(url, headers={
            "Content-Type": "application/json",
            "Authorization": get_access_token()
        })
        response.raise_for_status()
        content = response.json()
        return content["data"]
    except Exception as e:
        print(f"API Error: {str(e)}")
        return "Error: Making the tslFile request error"

def list_devices(product_key):
    base_url = os.environ.get('BASE_URL')
    url = f"{base_url}/v2/devicemgr/r3/openapi/product/device/overview?productKey={product_key}"
    try:
        response = requests.get(url, headers={
            "Content-Type": "application/json",
            "Authorization": get_access_token()
        })
        response.raise_for_status()
        content = response.json()
        return content["data"]
    except Exception as e:
        print(f"API Error: {str(e)}")
        return "Error: List devices error"

def power_switch(product_key, device_key, on_off):
    base_url = os.environ.get('BASE_URL')
    url = f"{base_url}/v2/deviceshadow/r3/openapi/dm/writeData"

    # Convert 'on'/'off' to 'true'/'false'
    switch_state = 'true' if on_off.lower() == 'on' else 'false'
    
    request_body = {
        "data": f'[{{"switch":"{switch_state}"}}]',
        "devices": [device_key],
        "productKey": product_key
    }
    #print(f'Request: {request_body}')
    
    try:
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": get_access_token()
            },
            json=request_body
        )
        response.raise_for_status()
        content = response.json()
        #print(f'Response: {content}')
        if content['code'] == 200 and content['data'][0]['code'] == 200:
            return "Success"
        else:
            return f"Error: {content['msg']}"
    except Exception as e:
        print(f"API Error: {str(e)}")
        return "Error: Failed to control device"