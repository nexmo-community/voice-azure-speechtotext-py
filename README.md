# Example code for connecting a Nexmo Voice API call to Azure Speech via websockets

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

You can use this code as a base for doing real time transcription on a phone call using [Azure Speech to Text API](https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/).

The Audio stream is sent over a websocket to your server and you then relay that on to the Azure websocket interface.

## Azure Speech to Text API

You'll need to signup for the Azure Speech to Text API, [start here](https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/).

### Prerequisites

To run this on your machine you'll need an [up-to-date version of Python 3](https://www.python.org/downloads/).

Start by installing the dependencies with:

```bash
pip install --upgrade -r requirements.txt
```

Next, edit the `server.py` file to add in your own service credentials from Azure and other settings specific to your instance of the Azure Speech Service API.

```python
HOSTNAME = 'example.ngrok.io'
LANGUAGE = "en-GB"
KEY1 = "1234567890abcdef"
PORT = 8000
REGIONAL_API_ENDPOINT = "westeurope"  # eg. westeurope, useast, southeastasia
```

Tools like [ngrok](https://ngrok.com/) are great for exposing ports on your local machine to the internet. If you haven't done this before, [check out this guide](https://www.nexmo.com/blog/2017/07/04/local-development-nexmo-ngrok-tunnel-dr/).

By default the server runs on port 8000, but you can change it to any other port should this conflict with anything else running on your local machine.

If you aren't going to be working in `en-GB` then you can change the language to any of the other supported languages listed in the [Speech Service API documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support).

The Azure Speech Service API can run across multiple regions. When you initially set it up you will specify which region your service will run in, you will then need to change the `REGIONAL_API_ENDPOINT` constant to match.

## Running the example

Run the server like this:

```bash
python ./server.py
```

## Linking the app to Nexmo

You will need to create a new application with the Nexmo CLI and set the answer_url as http://[YOUR HOSTNAME]/ncco and the event_url as http://[YOUR HOSTNAME]/event

The server will return an appropriate NCCO for this application, as specified in `ncco.json`.

Link a number to your application and then when you call the number you will be connected throgh to Azure, simply start talking and you should see results printed to the console.

## Extending

This example code simply prints the reponses from Azure to the console, however to integrate it with your own applicaiton you should extend the `on_return_message` function in [server.py](https://github.com/nexmo-community/voice-microsoft-speechtotext/blob/master/server.py#L119)
