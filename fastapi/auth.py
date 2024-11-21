from fastapi import HTTPException
import os


def validateToken(token):
    if token == os.environ["token"]:
        return True

    return HTTPException(status_code=401, detail="Invalid Token")
