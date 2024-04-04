import tornado
from common.auth import get_password_hash, verify_password
from common.handlers import BaseHandler
from common.schema import SignInRequest


class SignInHandler(BaseHandler):
    async def post(self):
        data = self.validate(SignInRequest)
        db_user = await self.db.users.find_one({'email': data.email})

        if db_user:
            # Verify password for exisiting users
            if not verify_password(data.password, db_user['password']):
                return tornado.web.HTTPError(401)

            user_id = str(db_user['_id'])
        else:
            # Create new account if user with the given email does not exist
            password_hash = get_password_hash(data.password)
            db_user = await self.db.users.insert_one(
                {
                    'email': data.email,
                    'password': password_hash
                }
            )
            user_id = str(db_user.inserted_id)

        self.set_signed_cookie(
            name='auth',
            value=user_id,
            httponly=True,
            secure=True,
        )
        self.write({
            'message': 'success'
        })

        return


class SignOutHandler(BaseHandler):
    def post(self):
        self.clear_cookie(
            name='auth',
            httponly=True,
            secure=True,
        )
        self.write({
            'message': 'success'
        })

        return
