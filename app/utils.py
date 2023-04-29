from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hassing_password(password: str):
    return pwd_context.hash(password)

def verify(plain_text:str,hashpassword):
    return pwd_context.verify(plain_text,hashpassword)