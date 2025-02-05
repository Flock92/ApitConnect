from apit212 import Apit212
import asyncio

if __name__ == "__main__":

    async def main():
        server = Apit212()

        # Start the server
        await server.run_server()

        # Start the main loop where all the bot logic goes
        try:
            print("Main thread is running...")
            while True: 
                await asyncio.sleep(5)
                msg = "hey this is it"
                await server.send_message(msg)
        except asyncio.CancelledError:
            print("Main thread stopped")

    #Run event loop
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
