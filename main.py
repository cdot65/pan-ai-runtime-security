#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from pprint import pprint

import aisecurity
from aisecurity.generated_openapi_client import Metadata
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile
from aisecurity.scan.models.content import Content
from aisecurity.scan.sync.scanner import Scanner
from dotenv import load_dotenv


# Load default profile name from environment variable
load_dotenv()

"""
Sdk setup

The aisecurity.init() function accepts the following parameters:
    1)api_key : Provide your API key through configuration or an environment variable.
    2)api_endpoint (optional): Default value is
    "https://service.api.aisecurity.paloaltonetworks.com".
    2)attempts (optional): Default value is 5.

Setting up the API Key:
Choose one of the following API Key Configuration Methods:
1) Using an environment variable:
    export PANW_AI_SEC_API_KEY=YOUR_API_KEY_GOES_HERE
2) Load Dynamically from a secure Secret Store (e.g. Cloud Secrets Manager / Vault)
    api_key = function_to_get_api_key() # TODO: Load an API Key at runtime
    aisecurity.init(api_key=api_key)


Customizing the API Endpoint
    aisecurity.init(api_endpoint="https://api.example.com")

"""

api_endpoint = os.environ.get(
    "PANW_AI_SEC_API_ENDPOINT",
    "https://service.api.aisecurity.paloaltonetworks.com"
)
aisecurity.init(api_endpoint=api_endpoint)

pprint("Create a new scanner")
ai_security_example = Scanner()

# Create AI profile and content objects
profile_name = os.environ.get("PANW_AI_PROFILE_NAME", None)
ai_profile = AiProfile(profile_name=profile_name)
content1 = Content(
    prompt="This is a tests prompt with 72zf6.rxqfd.com/i8xps1 url",
    response="This is a tests response",
)
# Optional parameters for the scan api
tr_id = "1234"  # Optionally Provide unique identifier for correlating transactions.
metadata = Metadata(
    app_name="concurrent_sdk", app_user="user", ai_model="sample_model"
)  # Optionally send the app_name, app_user, and ai_model in the metadata


pprint("==============================================================")
pprint("Invoke sync scan call")
scan_response = ai_security_example.sync_scan(
    ai_profile=ai_profile, content=content1, tr_id=tr_id, metadata=metadata
)
pprint("==============================================================")
"""
Sync scan example
    report_id='demo_report_id'
    scan_id='demo_scan_id'
    tr_id='demo_transaction_id'
    profile_id='demo_profile_id'
    profile_name='demo_profile_name'
    category='demo_category'
    action='demo_action'
    prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False)
    response_detected=ResponseDetected(url_cats=False, dlp=False)
    created_at=None
    completed_at=None
"""
pprint(f"sync scan response: {scan_response}\n")


if __name__ == "__main__":
    # Load environment variables from .env file
    # First try to load from current directory
    env_path = Path(".") / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        # If not found, try the script's directory
        script_dir = Path(__file__).parent.absolute()
        env_path = script_dir / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
        else:
            print("No .env file found in current directory or script directory")
            sys.exit(1)

    # Get credentials from environment variables with fallbacks
    pan_api_key = os.environ.get("PANW_AI_SEC_API_KEY", None)
    pan_api_endpoint = os.environ.get(
        "PANW_AI_SEC_API_ENDPOINT",
        "https://service.api.aisecurity.paloaltonetworks.com"
    )
    profile_name = os.environ.get("PANW_AI_PROFILE_NAME", None)
    log_level = os.environ.get("LOG_LEVEL", "DEBUG")

    # Validate required credentials
    if not all([pan_api_key]):
        missing = []
        if not pan_api_key:
            missing.append("PANW_AI_SEC_API_KEY")

        print(f"Missing required credentials: {', '.join(missing)}")
    else:
        print("All required credentials found")

    pprint("ai_security Example is completed")
