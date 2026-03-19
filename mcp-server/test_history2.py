from dotenv import load_dotenv
import os
import sys

# Force load .env from the exact same directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(env_path)

api_key = os.getenv("MODEXIA_API_KEY")
base_url = os.getenv("MODEXIA_BASE_URL", "https://sandbox.modexia.software")

sys.path.insert(0, "../../packages/SDKs/pythonSdk/src")
from modexia import ModexiaClient

client = ModexiaClient(api_key=api_key, base_url=base_url)
print(f"Testing get_history with base_url={base_url}")
try:
    print(client.get_history())
except Exception as e:
    import traceback
    traceback.print_exc()
