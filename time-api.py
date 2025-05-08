#setting up s simple server

from typing import Union

from fastapi import FastAPI # type: ignore

import time

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/time")
def read_time():
    time_in_seconds = time.time()
    current_time = time.ctime(time_in_seconds)
    return {"current date and time": current_time}
