from dotenv import load_dotenv
import os
import sys
load_dotenv(".env")
base_url = os.getenv("MODEXIA_BASE_URL", "https://sandbox.modexia.software")
api_key = os.getenv("MODEXIA_API_KEY")

sys.path.insert(0, "../../packages/SDKs/pythonSdk/src")
from modexia import ModexiaClient

print(f"Testing with base_url={base_url} and api_key={api_key}")
client = ModexiaClient(api_key=api_key, base_url=base_url)
try:
    print(client.get_history())
except Exception as e:
    import traceback
    traceback.print_exc()
