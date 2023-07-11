from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from app.db import database, Request

'''
    Notes about this implementation:
    
    All functions from db and functionality
    are together for convinience.

    
'''

app = FastAPI()

class DateResponse(BaseModel):
    date: str

@app.get("/requests")
async def read_root():
    """
    Get all the requests made.
    """
    return await Request.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.post("/date/")
async def get_date(include_time: bool):
    """
    Get the current date and time in the specified format.

    Parameters:
    - include_time (bool): If True, the response will include the time component (format: YYYY-MM-DD HH:MM:SS).
                           If False, only the date will be included (format: YYYY-DD-MM).

    Returns:
    - dict: A dictionary containing the formatted date.

    """
    
    current_date = datetime.now()
    if include_time:
        formatted_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        formatted_date = current_date.strftime("%Y-%d-%m")
        
    await Request.objects.create(returned_date=str(formatted_date))

    return {"date": formatted_date}

@app.get("/counter/")
async def get_counter():
    """
    Get the current value of the counter.
    """
    counter = len(await Request.objects.all())
    return {"counter": counter}