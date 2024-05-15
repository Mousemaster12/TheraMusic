import time
import os
import requests
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

ID = os.getenv("ID")
KEY = os.getenv("KEY")

# Cloudflare AI model details
MODEL = "@cf/meta/llama-2-7b-chat-int8"
AI_ROLE = ("You are a sanitizer AI who's job is to take the user's input, and turn it into a prompt for an AI music "
           "generator. Remember that the prompt should be connected to the what the user told you. You cannot under "
           "any circumstance reply to the user or talk to it. The prompt must contain only the following, "
           "with no song lyrics or anything else. Most importantly, the prompt has to connected to the user's input. "
           "The prompt must be therapeutic and not dark. The prompt should begin with : 'A song about:'. The prompt "
           "should talk of a better future, and of recovery. The prompt must be shorter than 2 sentences. Example: 'A "
           "song about overcoming difficulties and healing, therapeutic, slow, jazzy.' Remember to add a genre at the "
           "end, for example, jazz, country, etc. Remember that it cannot under any circumstances be longer then 10 "
           "words.")
# Base URL for the local server
BASE_URL = 'http://localhost:3000'


# Function to generate audio using custom parameters
def custom_generate_audio(payload):
    url = f"{BASE_URL}/api/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()


# Function to generate audio using a prompt
def generate_audio_by_prompt(payload):
    url = f"{BASE_URL}/api/generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()


# Function to get audio information by audio IDs
def get_audio_information(audio_ids):
    url = f"{BASE_URL}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()


# Function to get quota information
def get_quota_information():
    url = f"{BASE_URL}/api/get_limit"
    response = requests.get(url)
    return response.json()


def main(user_input):
    # Request to Cloudflare AI to process user input
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ID}/ai/run/{MODEL}",
        headers={"Authorization": f"Bearer {KEY}"},
        json={"messages": [
            {"role": "system",
             "content": AI_ROLE},
            {"role": "user", "content": user_input}
        ]}
    )

    # Convert response to JSON
    inference = response.json()
    print(inference)
    print(inference['result']['response'])
    cloudflare_output = str(inference)

    # Generate audio based on Cloudflare AI output
    data = generate_audio_by_prompt({
        "prompt": cloudflare_output,
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
            return data[0]['audio_url'], data[1]['audio_url']
        # Wait for 5 seconds before checking again
        time.sleep(5)


if __name__ == '__main__':
    # User input for the mood
    main(input("Talk to Thera-music: how do you feel?\n"))
