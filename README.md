# Speech To Text with Nexmo Voice API & Microsoft Azure

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://nexmo.dev/azure-nexmo-speechtotext-install) [![Remix on Glitch](https://cdn.glitch.com/2703baf2-b643-4da7-ab91-7ee2a2d00b5b%2Fremix-button.svg)](https://nexmo.dev/azure-nexmo-speechtotext-glitchremix) [![Deploy to Azure](https://azuredeploy.net/deploybutton.png)](https://azuredeploy.net)

You can use this code as a base for doing real time transcription of a phone call using [Azure Speech Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/).

An audio stream is sent over a websocket to your server and you then relay that on to the Azure websocket interface where recognition is performed and the phrases returned to the console.

## Azure Speech Services

You'll need to signup for [Azure Speech Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/) and make a note of two pieces of information - the first service API key, and the regional location of the Speech API service you deployed (eg. westeurope).

## Running the app

### Using Docker

To run the app using Docker run the following command in your terminal:

```bash
docker-compose up
```

This will create a new image with all the dependencies and run it at `http://localhost:8000`.

You can declare the required environment variables by editing the `docker-compose.yml` file.

### Local Install

To run this on your machine you'll need an [up-to-date version of Python 3](https://www.python.org/downloads/).

Start by installing the dependencies with:

```bash
pip install --upgrade -r requirements.txt
```

Then copy the `.env.example` file to a new file called `.env`:

```bash
cp .env.example > .env
```

Edit the `.env` file to add in your own service credentials from Azure and other settings specific to your instance of the Azure Speech Service API.

```python
HOSTNAME = "yourhostname.ngrok.io"
LANGUAGE = "en-GB"
KEY1 = "3234gh3gh34ghj32hj"
REGIONAL_API_ENDPOINT = "westeurope" # eg. "westeurope", "southeastasia", "uswest"
```

By default the server runs on port 8000.

Tools like [ngrok](https://ngrok.com/) are great for exposing ports on your local machine to the internet. If you haven't done this before, [check out this guide](https://www.nexmo.com/blog/2017/07/04/local-development-nexmo-ngrok-tunnel-dr/).

If you aren't going to be working in the `en-GB` language then you can change the language to any of the other supported languages listed in the [Speech Service API documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support).

The Azure Speech Service API can run across multiple regions. When you initially set it up you will specify which region your service will run in, you will then need to change the `REGIONAL_API_ENDPOINT` environment variable to match.

## Running the example

If you are working with a local install you can run the server using this command:

```bash
python ./server.py
```

## Linking the app to Nexmo

You will need to create a new Nexmo application in order to work with this app:

### Create a Nexmo Application Using the Command Line Interface

Install the CLI by following [these instructions](https://github.com/Nexmo/nexmo-cli#installation). Then create a new Nexmo application that also sets up your `answer_url` and `event_url` for the app running locally on your machine.

```bash
nexmo app:create ms-speech-to-text http://<your_hostname>/ncco http://<your_hostname>/event
```

This will return an application ID. Make a note of it.

### Rent a New Virtual Number

If you don't have a number already in place, you will need to rent one. This can also be achieved using the CLI by running this command:

```bash
nexmo number:buy
```

### Link the Virtual Number to the Application

Finally, link your new number to the application you created by running:

```bash
nexmo link:app YOUR_NUMBER YOUR_APPLICATION_ID
```

## Try it out

With your app running, call the number you assigned to it and start speaking. After a brief pause you will see whatever you say written out to the console, in real time.

## Extending

This example code simply prints the reponses from Azure to the console, however to integrate it with your own application you should extend the `on_return_message` function in [server.py](https://github.com/nexmo-community/voice-microsoft-speechtotext/blob/master/server.py#L117)
