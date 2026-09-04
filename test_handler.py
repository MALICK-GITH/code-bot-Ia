import json
from app import handler

# Test du handler
test_request = {
    'method': 'GET',
    'path': '/'
}

result = handler(test_request)
print("Handler test result:")
print(json.dumps(result, indent=2))