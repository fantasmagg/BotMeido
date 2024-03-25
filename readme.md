# Voice-Activated Email Assistant and Virtual Friend

This Python script combines speech recognition, text-to-speech, and email management functionalities to act as both a virtual assistant for email handling and a supportive virtual friend. Utilizing libraries such as `speech_recognition`, `pyttsx3`, `json`, `openai`, `os.path`, `base64`, and the Google API client, it offers a unique blend of practical utility and emotional support.

## Features

- **Voice Commands**: Interact with your assistant using natural speech.
- **Text-to-Speech Feedback**: Receive spoken responses for a seamless conversational experience.
- **Email Filtering and Reading**: Obtain emails from specific senders, prioritizing user-defined criteria.
- **Emotional Support**: Engage in conversations that are empathetic and supportive, akin to chatting with a friend.

## Setup and Installation

1. **Dependencies**: Ensure you have Python 3.6+ installed on your machine. Install the necessary Python libraries by running:
   ```bash
   pip install Speechrecognition pyttsx3 google-api-python-client google-auth-oauthlib google-auth-httplib2 openai
   ```
2. **Google API Credentials**: Follow the Google API Console documentation to set up a project with the Gmail API enabled. Download your credentials and save them as `token.json` in the project directory.
3. **OpenAI API Key**: Obtain an API key from OpenAI. Save this key in a file named `secretkey.txt`.
4. **Audio Device**: Ensure you have a working microphone set up on your system for speech recognition.

## How to Use

- **Start the Script**: Run the script in your terminal or command prompt with:
   ```bash
   python capturadorDeVoz.py
   ```
- **Speak to Your Assistant**: Begin interacting by speaking naturally. You can command the assistant to read your emails, filter them by sender, or simply engage in a friendly conversation.
- **Receive Spoken Responses**: The assistant will process your requests and provide feedback or perform actions accordingly.

## How It Works

- The script initializes the speech recognition and text-to-speech engines, setting properties for voice type and speaking rate.
- It listens for audio input from the user, converts speech to text, and processes the request.
- For email-related tasks, it filters and fetches emails from your Gmail account based on specified criteria.
- Utilizes the OpenAI API to generate conversational responses, incorporating predefined functions like email retrieval into the chat context.

## Customization

- **Voice and Speech Rate**: Modify the `engine.setProperty` calls to change the voice and speed of the assistant's speech.
- **Functionality**: Extend the `functions` list and implement additional functions in the script to enhance the assistant's capabilities.
