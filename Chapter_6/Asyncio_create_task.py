import uasyncio as asyncio 
from time import *

async def time_test1():
    print("Start task 1 at :", ticks_ms()) 
    await asyncio.sleep(2)
   
    

async def time_test2():
    print("Start task 2 at :", ticks_ms()) 
    await asyncio.sleep(2)
 

async def main():
    time_start = ticks_ms()
    print("Start task at : ", time_start) 
    one = asyncio.create_task(time_test1())
    two = asyncio.create_task(time_test2())
    await one
    await two 
    time_end = ticks_ms()
    print("End task at : ", time_start) 
    print("total time spend : ", time_end - time_start )
    

asyncio.run(main())