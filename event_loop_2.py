import asyncio

def simple_callback():
    print("The callback was executed by the loop!")

# 1. Manually create the loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 2. Schedule a standard Python function to run "soon" (in the next iteration)
loop.call_soon(simple_callback)

# 3. Start the loop. (We use stop() inside call_soon just so this script actually ends)
loop.call_soon(loop.stop)

print("Starting loop...")
loop.run_forever()
print("Loop stopped.")
loop.close()
