from common.auth import authenticated
from common.handlers import BaseHandler
from common.speech import speechToText


class SpeechToTextHandler(BaseHandler):
    @authenticated
    def post(self):

        audio = self.request.files['audio'][0].get('body')
        text = speechToText(audio)

        self.write({
            'text': text
        })
