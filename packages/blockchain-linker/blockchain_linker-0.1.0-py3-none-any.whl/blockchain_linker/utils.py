import hashlib
import json
import time
from typing import Any

def calculate_hash(data: Any) -> str:
    data_string = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(data_string).hexdigest()

def get_timestamp() -> float:
    return time.time() 