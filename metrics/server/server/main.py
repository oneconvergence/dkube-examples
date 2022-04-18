from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from .schema import *
import json
import csv
import time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

reader = csv.DictReader(open("server/metrics.csv"))
metrics = [row for row in reader]
index = 0

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise credentials_exception

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # authenticate with username, password here
    data={"sub": form_data.username}
    data.update({"expire": str(datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}

@app.post("/query_range", response_model=MetricResponse)
async def get_metrics(request: MetricRangeRequest, current_user: str = Depends(get_current_user)):
    global index
    metric = metrics[index % len(metrics)]
    index += 1
    data = []
    timestamp = time.time()
    for k,v in metric.items():
        data.append({"metric":{"name":k}, "values": [[timestamp, v]]})
    return {"status": "success", "data": data}
