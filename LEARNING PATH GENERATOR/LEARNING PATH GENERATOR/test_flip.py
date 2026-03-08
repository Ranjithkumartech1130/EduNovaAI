import requests
import json

def test_arithmetic_flip():
    url = "http://127.0.0.1:5000/evaluate"
    payload = {
        "algorithm": "Start Read two numbers a and b Compute sum = a - b Display sum Stop",
        "language": "python"
    }
    
    print(f"🚀 Testing logic flip detection...")
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_arithmetic_flip()
