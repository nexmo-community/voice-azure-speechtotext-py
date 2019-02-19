import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import gen
import json
import requests
import os
from string import Template
from uuid import uuid4
import datetime


HOSTNAME = 'example.ngrok.io'  # Change to the hostname of your server
LANGUAGE = "en-GB"
KEY1 = "1234567890abcdef"
PORT = 8000


def get_token():
    url = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {'Ocp-Apim-Subscription-Key': KEY1}
    resp = requests.post(url, headers=headers)
    token = None
    if resp.status_code == 200:
        token = resp.content
    else:
        print(resp.status_code)
        print(resp.content)
    return token


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.content_type = 'text/plain'
        self.write("Microsoft STT Example")
        self.finish()


class CallHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        data = {}
        data['hostname'] = HOSTNAME
        filein = open('ncco.json')
        src = Template(filein.read())
        filein.close()
        ncco = json.loads(src.substitute(data))
        self.write(json.dumps(ncco))
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.finish()


class EventHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        print(self.request.body)
        self.content_type = 'text/plain'
        self.write('ok')
        self.finish()


class WSHandler(tornado.websocket.WebSocketHandler):
    watson_future = None
    req_id = str(uuid4().hex)

    def open(self):
        token = get_token()
        print("Websocket Call Connected")
        req = tornado.httpclient.HTTPRequest("wss://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1?format=simple&language=" +
                                             LANGUAGE, headers={'X-ConnectionId': str(uuid4().hex), 'Authorization': token})
        self.azure_future = tornado.websocket.websocket_connect(
            req, on_message_callback=self.on_return_message)

    @gen.coroutine
    def on_message(self, message):
        azure = yield self.azure_future
        if type(message) != str:
            headers = """path: audio\r\ncontent-type: audio/x-wav\r\nx-requestid: {}\r\nx-timestamp: {}\r\n\r\n""".format(
                self.req_id, datetime.datetime.utcnow().isoformat())
            b_headers = bytes(headers, "ascii")
            hlen = len(headers).to_bytes(2, byteorder='big')
            data = hlen+b_headers+message
            azure.write_message(data, binary=True)
        else:
            headers = """path: speech.config\r\ncontent-type: application/json\r\nx-xequestid: {}\r\nx-timestamp: {}\r\n\r\n""".format(
                str(uuid4().hex), datetime.datetime.utcnow().isoformat())
            config = {
                "context": {
                    "system": {
                        "version": "0.1",
                    },
                    "os": {
                        "platform": "PSTN",
                        "name": "Phone",
                        "version": "1.0"
                    },
                    "device": {
                        "manufacturer": "Nexmo",
                        "model": "VAPI",
                        "version": "1.0"
                    }
                },
            }
            data = headers+json.dumps(config)
            azure.write_message(data, binary=False)

    @gen.coroutine
    def on_close(self):
        print("Websocket Call Disconnected")
        azure = yield self.azure_future
        azure.close()

    def on_return_message(self, message):
        if message != None:
            headers = {}
            headerdata = message.split("\r\n\r\n")[0].split("\n")
            for line in headerdata:
                h = line.split(":")
                headers[h[0]] = h[1]
            body = "\r\n\r\n".join(message.split("\r\n\r\n")[1:])
            if headers["Path"] == "turn.end":
                self.req_id = str(uuid4().hex)
            if headers["Path"] == "speech.phrase":
                data = json.loads(body)
                if data['RecognitionStatus'] == "Success":
                    # Extend From here to handle your transcription messages
                    print(data["DisplayText"])


def main():
    static_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'static')
    application = tornado.web.Application([(r"/", MainHandler),
                                           (r"/event", EventHandler),
                                           (r"/ncco", CallHandler),
                                           (r"/socket", WSHandler),
                                           (r'/static/(.*)', tornado.web.StaticFileHandler,
                                            {'path': static_path}),
                                           ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", PORT))
    print(f"Server running on port {PORT}")
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
