import os
from typing import Union
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

    def get_current_user(self) -> Union[str, None]:
        user = self.get_signed_cookie('auth')
        if user is not None:
            user = str(user)

        return user

    def set_default_headers(self) -> None:
        self.set_header(
            'Access-Control-Allow-Origin', os.environ['CORS_ORIGIN']
        )
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Credentials', 'true')

        return

    def validate(self, schema: BaseModel) -> BaseModel:
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
