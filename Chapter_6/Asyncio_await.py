import uasyncio as asyncio 
from time import *

async def time_test(): 
    time_start = ticks_ms()
    print("Start task at :  ", time_start)
    print("Start task 1 at :", ticks_ms()) 
    await asyncio.sleep_ms(2000)
    print("Start task 2 at :", ticks_ms()) 
    await asyncio.sleep_ms(2000)
    time_end = ticks_ms()
    print("End task at : ", time_start) 
    print("total time spend : ", time_end - time_start )
    
asyncio.run(time_test())