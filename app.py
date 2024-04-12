import asyncio
import os

from dotenv import load_dotenv
import motor
import tornado

from handlers.auth import SignInHandler, SignOutHandler
from handlers.sst import SpeechToTextHandler
from handlers.stories import ListenStoryHandler, StoriesHandler, StoryHandler

load_dotenv()

client = motor.motor_tornado.MotorClient(os.environ['MONGODB_URL'])
db = client[os.environ['DB_NAME']]


class Application(tornado.web.Application):
    def __init__(self, db: motor.MotorDatabase):
        handlers = [
            (r'/api/auth/sign-in', SignInHandler, dict(db=db)),
            (r'/api/auth/sign-out', SignOutHandler),
            (r'/api/stories', StoriesHandler, dict(db=db)),
            (r'/api/stories/([^/]+)', StoryHandler, dict(db=db)),
            (r'/api/stories/([^/]+)/listen', ListenStoryHandler, dict(db=db)),
            (r'/api/sst', SpeechToTextHandler),
        ]

        settings = dict(
            cookie_secret=os.environ['COOKIE_SECRET'],
            debug=(os.environ['ENV'] == 'dev'),
        )

        super().__init__(handlers, **settings)


async def main():
    app = Application(db)
    app.listen(8080)
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
