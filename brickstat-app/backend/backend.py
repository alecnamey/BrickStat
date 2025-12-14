import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("REBRICKABLE_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "REBRICKABLE_API_KEY not set. "
        "Did you forget to create a .env file or export it?"
    )

BASE_URL = "https://rebrickable.com/api/v3/lego/sets/"

def get_set_by_number(set_num):
    headers = {
        "Authorization": f"key {API_KEY}"
    }

    url = f"{BASE_URL}{set_num}/"
    response = requests.get(url, headers=headers, timeout=5)

    if response.status_code == 404:
        print("Invalid set number. Format should look like 75257-1.")
        return

    response.raise_for_status()

    s = response.json()

    print("\n=== LEGO SET FOUND ===")
    print(f"Name: {s['name']}")
    print(f"Set: {s['set_num']}")
    print(f"Year: {s['year']}")
    print(f"Pieces: {s['num_parts']}")
    print(f"Image: {s['set_img_url']}")
    print("=====================\n")

if __name__ == "__main__":
    while True:
        set_number = input(
            "Enter a set number (e.g. 75257-1) or 'exit': "
        ).strip()

        if set_number.lower() == "exit":
            print("Goodbye")
            break

        get_set_by_number(set_number)
