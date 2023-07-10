from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

'''
    Notes about this implementation:
    
    This is the most trivial solution,
    using a global variable.
    
    Disadvantages: If the service is down,
    the information about the number of 
    times it was called will be lost.
    
'''

app = FastAPI()
counter = 0

class DateResponse(BaseModel):
    date: str


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
    global counter 
    counter += 1
    
    current_date = datetime.now()
    if include_time:
        formatted_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        formatted_date = current_date.strftime("%Y-%d-%m")

    return {"date": formatted_date}

@app.get("/counter/")
async def get_counter():
    """
    Get the current value of the counter.
    """
    return {"counter": counter}