import asyncio

def callback():
    print("Callback executed by the event loop.")


# 1. Manually creating an event loop
loop = asyncio.get_event_loop()

# 2. Scheduling a callback to be executed by the event loop
loop.call_soon(callback)

# Notice that call_soon doesn't block.
# It merely appends the function to the loop's internal queue.

# 3. Start the loop. (We use stop() inside call_soon just so this script actually ends)
loop.call_soon(loop.stop)

# 4. Run the event loop until stop() is called
# The execution only happens when loop.run_forever() takes over the main thread.
loop.run_forever()

print("Event loop has stopped.")
loop.close()
