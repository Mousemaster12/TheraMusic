# Theramusic Python Script Overview

This Python script interacts with the unofficial gcui-art/suno-api API and Cloudflare AI to generate therapeutic music based on user input. It utilizes different functions to communicate with the server and Cloudflare AI, generating audio based on user-provided mood or emotion.
Requirements

    Python 3.x
    Requests library (for making HTTP requests)
    JSON library (for handling JSON data)
    Time library (for adding delays)
    The gcui-art/suno-api up and running
    pygame for GUI (under development)

## Setup

  Install Python if not already installed. You can download it from here.
  Install the Requests library and pygame using pip:

    pip install requests
    pip install pygame

## Usage

  Run the script in a Python environment.
  Enter the user's mood or emotion when prompted.
  The script will generate a prompt for Cloudflare AI based on the user input, and then generate therapeutic music.
  The generated audio will be streamed after a short delay.

## Functions

    custom_generate_audio(payload): Generates audio using custom parameters.
    generate_audio_by_prompt(payload): Generates audio using a prompt.
    get_audio_information(audio_ids): Retrieves audio information by audio IDs.
    get_quota_information(): Retrieves quota information.

## Cloudflare AI Model

  The script utilizes a Cloudflare AI model (@cf/meta/llama-2-7b-chat-int8) to process user input and generate prompts for the music generator.

## Notes

  Ensure that the local server is running and accessible at http://localhost:3000.
  Cloudflare AI authentication details (ID and KEY) must be provided for accessing the Cloudflare AI model.
  The generated prompt should be therapeutic, optimistic, and relevant to the user's input.
  The script waits for the audio to be generated and streamed before displaying the audio URLs.

Author

    [Your Name/Contact Information]
