from apit212 import Apit212
import signal
import asyncio

if __name__ == "__main__":

    async def main():
        server = Apit212()
        cfd = server.CFD(mode="demo")


        def signal_handler(sig, frame):
            print('You pressed Ctrl+C!')
            asyncio.create_task(server.stop_server())
            

        signal.signal(signal.SIGINT, signal_handler)
        print('Press Ctrl+C')
        
        #signal.signal(signal, server.stop_server)

        # Start the server
        await server.run_server()

        # Start the main loop where all the bot logic goes
        try:
            print("Main thread is running...")
            while True: 
                await asyncio.sleep(2)
                msg = "hey this is it"
                await server.send_message(msg)
                if server.messages.empty() != True:
                    msg = await server.fetch_message()
                    print(f"Message recieved: {msg}")
                # user_input = input("Try input a command: ")
                # match user_input:
                #     case "summary":
                #         print(cfd.get_summary())
                #         print("fetch summary")
                #     case "account":
                #         print("fetch account")
                #     case "quit":
                #         await server.stop_server()
                #         break
                #     case _:
                #         print("Unknown command!")
                # del user_input
                # await server.stop_server()
                if server.server == None:
                    print("loop closed")
                    break
        except asyncio.CancelledError:
            print("Main thread stopped")

    # run the loop
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
