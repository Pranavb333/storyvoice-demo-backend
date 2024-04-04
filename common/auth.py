import bcrypt


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
