from apit212 import Apit212, CFDRequest
import signal
import asyncio
import json


SERVER_TASK = asyncio.Queue()

APIT_SERVER = Apit212()
CFD = CFDRequest(mode="demo")

# HANDLE CLTR + C (CLOSE SERVER)
def close_server(signal, frame):
    if APIT_SERVER.server != None:
        asyncio.create_task(APIT_SERVER.stop_server())

# SEND MESSAGE USING SERVER FUNC
async def send_msg(msg: dict) -> None:
    if APIT_SERVER.server != None:
        await APIT_SERVER.send_message(msg)

# CREATE A TRADING LOOP THAT CHECK PRICES AND CREATES TASK
async def trade_loop():

    print("running trading loop")
    while True:

        if len(APIT_SERVER.client_connections) > 0:

            await asyncio.sleep(0.1)

            if APIT_SERVER.server == None:
                break

            trade = {"notify":"NONE","quantity":-400, "limitDistance":0.012, 
                     "stopDistance":0.012, "instrumentCode":"GBPUSD","targetPrice":1.2}

            trade_task = {"instruction":"trade", "command":"open_position", "mode": "demo", "data": trade}
            await SERVER_TASK.put(trade_task)
            
        else:
            await asyncio.sleep(1)

            if APIT_SERVER.server == None:
                print("closing trading loop!")
                break

# CREATE THE MAIN LOOP 
async def main():

    # SIGNAL HANDLER (close server)
    signal.signal(signal.SIGINT, close_server)

    # START PYTHON SERVER
    await APIT_SERVER.run_server()

    # RUN USERS MAIN LOOP
    print("Starting Main Loop")

    try:

        while True:

            await asyncio.sleep(1)

            # CHECK IF SERVER IS STILL RUNNING
            if APIT_SERVER.server == None:
                print("Server Closed Main Loop Ended!")
                break

            # CHECK FOR ANY MESSAGES ON SERVER
            if APIT_SERVER.messages.empty() != True:
                response = await APIT_SERVER.fetch_message()
                print(f"Message Recieved: {response}")

            # CHECK FOR ANY LOCAL TASK TO COMPLETE
            if SERVER_TASK.empty() != True and len(APIT_SERVER.client_connections) != 0:

                for i in range(SERVER_TASK.qsize()):

                    if APIT_SERVER.client_connections == 0:
                        print("connection dropped: task proccess stopped")
                        break
                    
                    task = await SERVER_TASK.get() # fetch task from the task queue

                    match task["instruction"]:

                        case "trade":
                            await send_msg(task)
                            # print("sending order")
                            pass

                        case "end_trading":
                            await APIT_SERVER.stop_server()

                        case _:
                            pass   

    except asyncio.CancelledError as em:
        print(f"MainLoop Error: {em}")

    await asyncio.sleep(5)


if __name__ == "__main__":

    # CREATE AND START EVENT LOOP
    event_loop = asyncio.new_event_loop()
    event_loop.create_task(trade_loop())
    event_loop.run_until_complete(main())
