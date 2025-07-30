from mcp.server.fastmcp import FastMCP
from typing import Dict
import requests
import os
import uuid
import re

mcp = FastMCP("Lyzr Single Tool")


def sanitize_agent_name(agent_name):
    # Remove all characters except a-z, A-Z, 0-9, _ and -
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "", agent_name)
    # Trim to a max length of 64 characters
    return sanitized[:64]


api_key = os.getenv("LYZR_API_KEY")
user_id = os.getenv("LYZR_USER_ID")
agent_id = os.getenv("LYZR_AGENT_ID")

# Validate environment variables
if not api_key or not user_id or not agent_id:
    raise ValueError("Missing environment variables")


# Get Agent data
def get_agent_data():
    url = f"https://agent-prod.studio.lyzr.ai/v3/agents/{agent_id}"
    headers = {"Content-Type": "application/json", "x-api-key": api_key}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"API request failed with status {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


agent_data = get_agent_data()


@mcp.tool(
    name=sanitize_agent_name(agent_data["name"]),
    description=agent_data["description"],
)
def send_agent_message(message: str) -> dict:
    session_id = f"{agent_id}-{str(uuid.uuid4())[:8]}"

    # API request setup
    url = "https://agent-prod.studio.lyzr.ai/v3/inference/chat/"
    headers = {"Content-Type": "application/json", "x-api-key": api_key}
    payload = {
        "user_id": user_id,
        "agent_id": agent_id,
        "session_id": session_id,
        "message": message,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"API request failed with status {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


def main():
    mcp.run(transport="stdio")
