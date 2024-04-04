from motor import MotorDatabase
from pydantic import BaseModel, ValidationError
import tornado


class BaseHandler(tornado.web.RequestHandler):
    '''
    Extends tornado.web.RequestHandler

    Passes db to all class methods
    Adds method to validate request body
    '''
    def initialize(self, db: MotorDatabase = None):
        self.db = db

    def validate(self, schema: BaseModel):
        '''
        Validates the request body as JSON using a pydantic model
        '''
        json = tornado.escape.json_decode(self.request.body)

        try:
            data = schema(**json)

            return data

        except ValidationError as e:
            detail = e.errors(
                include_url=False, include_context=False, include_input=False
            )

            self.set_status(422)
            self.write({
                'detail': detail
            })
            self.finish()
