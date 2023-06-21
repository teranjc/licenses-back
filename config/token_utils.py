from jwt import encode,decode
from jwt import  exceptions
from datetime import datetime,timedelta
from os import getenv
from fastapi.responses import JSONResponse
def expite_date(days:int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date

def write_token(data:dict):
    token = encode(payload={**data, "exp":expite_date(2)}, key=getenv("SECRET_KEY"),algorithm="HS256")
    return token


def validate_token(token,output=False):
    try:
        if output:
            decode(token,key=getenv("SECRET_KEY"),algorithms=["HS256"])
        decode(token, key=getenv("SECRET_KEY"), algorithms=["HS256"])
    except exceptions.DecodeError:
        return JSONResponse(content={"message":"invalid token"},status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message":"Token expired"},status_code=401)