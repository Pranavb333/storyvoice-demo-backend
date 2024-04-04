import asyncio
import os

from dotenv import load_dotenv
import motor
import tornado

from handlers.auth import SignInHandler, SignOutHandler

load_dotenv('.env.local')

client = motor.motor_tornado.MotorClient(os.environ['MONGODB_URL'])
db = client[os.environ['DB_NAME']]


class Application(tornado.web.Application):
    def __init__(self, db: motor.MotorDatabase):
        handlers = [
            (r'/auth/sign-in', SignInHandler, dict(db=db)),
            (r'/auth/sign-out', SignOutHandler),
        ]

        settings = dict(
            cookie_secret=os.environ['COOKIE_SECRET'],
        )

        super().__init__(handlers, **settings)


async def main():
    app = Application(db)
    app.listen(8080)
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
