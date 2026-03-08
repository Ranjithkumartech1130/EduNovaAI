import requests
import json

def test_evaluation():
    url = "http://127.0.0.1:5000/evaluate"
    payload = {
        "algorithm": "def find_max(arr):\n    max_val = arr[0]\n    for x in arr:\n        if x > max_val: max_val = x\n    return max_val",
        "language": "python"
    }
    
    print(f"🚀 Sending request to {url}...")
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            print("✅ Success! Feedback received:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_evaluation()
