import os
import time
import hashlib
import urllib.parse
import requests
from dotenv import load_dotenv

from iot_mcp_server import util

def main():
    # Load environment variables
    load_dotenv()

    os.environ["BASE_URL"] = "https://iot-api.quectelcn.com"
    os.environ["ACCESS_KEY"] = "24b9zq36CtkVFHSiBW9aMeLF"
    os.environ["ACCESS_SECRET"] = "6AUSH6PmD22dYjMLonHuiKEp5S83GkQ83epBbDqG"
    #os.environ["PRODUCT_KEY"] = "p11u3h"
    #os.environ["PRODUCT_KEY"] = "p11vfE"

    # list products
    products = util.list_products()
    print(products)

    ## get product tsl json
    #product_key = os.environ.get('PRODUCT_KEY')
    #tsl_json = util.get_product_tsl_json(product_key)
    #print(tsl_json)

    ## list devices
    #product_key = 'p11u3h'
    #devices = util.list_devices(product_key)
    #print(devices)

    ## get property from device
    ## not working yet!!!
    #product_key = 'p11u3h'
    #device_key = 'VDU4198'
    #property_code = 'switch'
    #value = util.read_device_property(product_key, device_key, property_code)
    #print(value)

