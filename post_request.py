import requests
import os


class PostRequest:
    def __init__(self, channel, value1, value2=None):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.channel = channel
        self.value1 = value1
        self.value2 = value2
        self.key = open(os.path.join(__location__, 'webhook_key')).readline()

    def send(self):
        url = "https://maker.ifttt.com/trigger/{}/with/key/{}".format(self.channel, self.key)
        message = {
            "value1": self.value1,
            "value2": self.value2
        }
        requests.post(url, data=message)
