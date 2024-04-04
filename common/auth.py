import bcrypt
import functools

from common.handlers import BaseHandler


def get_password_hash(password: str) -> str:
    '''
    Returns hashed password
    '''

    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(bytes, salt).decode('utf')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''
    Compares plain text password to hashed password
    '''

    return bcrypt.checkpw(
        plain_password.encode('utf-8'), hashed_password.encode('utf-8')
    )


def authenticated(method, *args, **kwargs):
    '''
    Decorates methods with this to require that the user be signed in

    If user is not signed in, it will raise a HTTP 401 error
    '''
    @functools.wraps(method)
    def wrapper(self: BaseHandler):
        if not self.current_user:
            self.set_status(401)
            self.write({'detail': 'Please sign-in to continue'})
            self.finish()

            return

        return method(self, *args, **kwargs)

    return wrapper
