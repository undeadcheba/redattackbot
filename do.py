import requests
import datetime
import os
#greet_bot = BotHandler(os.environ['BOT_TOKEN'])

URL = "https://api.telegram.org/bot%s/" % os.environ['BOT_TOKEN']
MyURL = "https://redattackbot.herokuapp.com/hook"

api = requests.Session()
application = tornado.web.Application([
    (r"/", Handler),
])

class Handler(tornado.web.RequestHandler):
        def post(self):
            try:
                logging.debug("Got request: %s" % self.request.body)
                update = tornado.escape.json_decode(self.request.body)
                message = update['message']
                text = message.get('text')
                if text:
                    logging.info("MESSAGE\t%s\t%s" % (message['chat']['id'], text))

                    if text[0] == '/':
                        command, *arguments = text.split(" ", 1)
                        response = CMD.get(command, not_found)(arguments, message)
                        logging.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
                        send_reply(response)
            except Exception as e:
                logging.warning(str(e))
                
         def send_reply(response):
    		if 'text' in response:
        		api.post(URL + "sendMessage", data=response)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    try:
        set_hook = api.get(URL + "setWebhook?url=%s" % MyURL)
        if set_hook.status_code != 200:
            logging.error("Can't set hook: %s. Quit." % set_hook.text)
            exit(1)
        application.listen(8888)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        signal_term_handler(signal.SIGTERM, None)
