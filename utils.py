import os
from mlhub.pkg import get_private


# ----------------------------------------------------------------------
# Request subscription key and endpoint from user.
# ----------------------------------------------------------------------

def request_priv_info():
    PRIVATE_FILE = "private.json"

    path = os.path.join(os.getcwd(), PRIVATE_FILE)

    private_dic = get_private(path, "aztext")

    subscription_key = private_dic["Text Analytics"]["key"]

    endpoint = private_dic["Text Analytics"]["endpoint"]
    return subscription_key, endpoint
