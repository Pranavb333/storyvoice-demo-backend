import os

from dotenv import load_dotenv
import motor

load_dotenv('.env.local')

client = motor.motor_tornado.MotorClient(os.environ['MONGODB_URL'])
db = client[os.environ['DB_NAME']]

db.users.create_index('email')
