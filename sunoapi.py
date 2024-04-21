import time
import requests
import json

# Base URL for the local server
base_url = 'http://localhost:3000'

# Function to generate audio using custom parameters
def custom_generate_audio(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

# Function to generate audio using a prompt
def generate_audio_by_prompt(payload):
    url = f"{base_url}/api/generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

# Function to get audio information by audio IDs
def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()

# Function to get quota information
def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = requests.get(url)
    return response.json()

if __name__ == '__main__':
    # User input for the mood
    userinput = input("Talk to Theramusic: how do you feel?\n")

    # Cloudflare AI model details
    model = "@cf/meta/llama-2-7b-chat-int8"
    ID = "bdeec1ca2606bf703bdbea35c03445e6"
    KEY = "g_HTKCSaRI3__BSlGGeQf5TR_ZgZ4yWi5u8BDxti"

    # Request to Cloudflare AI to process user input
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ID}/ai/run/{model}",
        headers={"Authorization": f"Bearer {KEY}"},
        json={"messages": [
            {"role": "system", "content": "You are a santizer ai whos job is to take the user's input, and turn it into a prompt for an ai music generator. remember that the prompt should be connected to the what the user told you. you cannot under any circumstance repy to the user or talk to it. the prompt must contain only the following, with no song lyrics or anything else. most important, the prompt has to connected to the user's input. The prompt must be theraputic and not dark. The pormpt should begin with : 'A song about:'. the prompt should talk of a better future, and of recovery. the prompt must be shorter then 2 sentances example: A song about overcoming diffuclties and healing, theraputic, slow, jazzy. remember to add a genre at the end for example, jazz, country, etc. remember that it cannot under any circumstances be longer then 10 words"  },
            {"role": "user", "content": userinput}
        ]}
    )
 
    # Convert response to JSON
    inference = response.json()
    print(inference)
    cloudflareout = str(inference)
    
    # Generate audio based on Cloudflare AI output
    data = generate_audio_by_prompt({
        "prompt": cloudflareout,
        "make_instrumental": False,
        "wait_audio": False
    })

    # Extract audio IDs
    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"ids: {ids}")

    # Check audio status and get audio URLs
    for _ in range(60):
        data = get_audio_information(ids)
        if data[0]["status"] == 'streaming':
            print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
            print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
            break
        # Wait for 5 seconds before checking again
        time.sleep(5)
