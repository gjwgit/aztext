import os
from mlhub.pkg import get_private


# ----------------------------------------------------------------------
# Request subscription key and endpoint from user.
# ----------------------------------------------------------------------

def request_priv_info():
    PRIVATE_FILE = "private.json"

    path = os.path.join(os.getcwd(), PRIVATE_FILE)

    key, endpoint = get_private(path, "Text Analytics")

    return key, endpoint
