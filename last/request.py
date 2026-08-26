import requests

response = requests.post(
    "https://tokengate-cqt9ivzs.manus.space/v1/chat/completions",
    headers={
        "Authorization": f"Bearer tf_live_3jKRMPIsj-9TvtTU4PYsUHOXuf7n23PJEjGbArizDm4",
        "Content-Type": "application/json",
    },
    json={
        "model": "claude-opus-5",
        "messages": [
            {
                "role": "user",
                "content": "Раскажи о теории струн"
            }
        ],
        "stream": False
    },
    timeout=110,
)

response.raise_for_status()

data = response.json()

print()
print(response.status_code, data)
print(data['choices'][0]['message']['content'])
