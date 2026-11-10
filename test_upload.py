"""
Test script - sends test_car.jpg to the ALPR endpoint and prints the result.
Usage: python test_upload.py [image_path] [api_url]
"""

import sys
import os

IMAGE_PATH = sys.argv[1] if len(sys.argv) > 1 else "test_car.jpg"
API_URL = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("ALPR_API_URL", "http://localhost:8000/recognize-plate")


def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"ERROR: Image file '{IMAGE_PATH}' not found.")
        sys.exit(1)

    print(f"Sending '{IMAGE_PATH}' to {API_URL}...")

    # Support httpx (default project dependency) or requests
    try:
        import httpx
        with open(IMAGE_PATH, "rb") as f:
            files = {"file": (os.path.basename(IMAGE_PATH), f, "image/jpeg")}
            with httpx.Client(timeout=35) as client:
                resp = client.post(API_URL, files=files)
                status_code = resp.status_code
                data = resp.json()
    except ImportError:
        try:
            import requests
            with open(IMAGE_PATH, "rb") as f:
                files = {"file": (os.path.basename(IMAGE_PATH), f, "image/jpeg")}
                resp = requests.post(API_URL, files=files, timeout=35)
                status_code = resp.status_code
                data = resp.json()
        except ImportError:
            print("ERROR: Neither 'httpx' nor 'requests' is installed. Run: pip install httpx")
            sys.exit(1)
    except Exception as exc:
        print(f"ERROR: Cannot connect to {API_URL}: {exc}")
        print("Is the ALPR server running? (Start with: uvicorn main:app --reload)")
        sys.exit(1)

    print(f"Status Code : {status_code}")
    print(f"Response    : {data}")

    if status_code == 200:
        print(f"\n  Plate Text : {data.get('plate_text')}")
        print(f"  DB Success : {data.get('db_success')}")
        print(f"  Message    : {data.get('message')}")
        sys.exit(0)
    else:
        print(f"\nRequest failed with status {status_code}: {data.get('detail', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
