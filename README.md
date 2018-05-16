# Example code for connecting a Nexmo Voice API call to Azure Speech via websockets

You can use this code as a base for doing real time transcription on a phone call using Azure Speech to Text API.

The Audio stream is sent over a websocket to your server and you then relay that on to the Azure websocket interface.

## Running the example

To run this on your machine you'll need an up-to-date version of Python 3. Install dependencies with:

```bash
pip install --upgrade -r requirements.txt
```

You'll need to edit the `server.py` file to add in your own service credentials from azure and also specify the hostname where your machine is running, tools like ngrok are great for exposing your local machine to the internet. You may also want to change the language from en-GB.

By default the server runs on port 8000


Run the server like this:
```bash
python ./server.py 

```

## Linking to Nexmo 
You will need to create a new application with the Nexmo CLI and set the answer_url as http://[YOUR HOSTNAME]/ncco and the event_url as  http://[YOUR HOSTNAME]/event
The server will return an appropriate NCCO.
Link a number to your application and then when you call the number you will be connected throgh to Azure, simply start talking and you should see results printed to the console.


## Extending 
This example code simply prints the reponses from Azure to the console, however to integrate it with your own applicaiton you should extend the `on_Azure_message` [function in server.py](https://github.com/nexmo-community/voice-microsoft-speechtotext/blob/master/server.py#L119)
