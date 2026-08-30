import requests

KEY = "sk-XrNHMSmCMwFYo1CvWbHEDz7tf5LXhNwOCho6F7CA1oQcTFo7"

response = requests.post(
    "https://seekai.cc/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "gemini-3-6-flash",
        "messages": [
            {
                "role": "user",
                "content": "Review this service architecture for reliability, security, and scalability. State the highest-impact risks first, then give a staged remediation plan."
            }
        ]
    },
    timeout=110,
)

print(response.json())
