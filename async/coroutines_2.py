import asyncio

async def fetch_data(delay, result):
    print(f"[Coro] Fetching data (simulating {delay}s delay)...")
    # asyncio.sleep() returns a Future that resolves after 'delay' seconds
    await asyncio.sleep(delay) 
    print(f"[Coro] Data fetched: {result}")
    return result

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 1. Create the coroutine
coro = fetch_data(1.5, "Database Record 42")

# 2. Wrap it in a Task. 
# This instantly schedules Task._step via loop.call_soon()
my_task = loop.create_task(coro)

print(f"Task state before loop: {my_task._state}")

# 3. my_task is a Future. We can tell the loop to run until this Future is FINISHED.
print("Starting event loop...")
final_result = loop.run_until_complete(my_task)

print(f"Task state after loop: {my_task._state}")
print(f"Loop returned: {final_result}")

loop.close()


"""
In all of these examples, only one thread is involved.

This is often the biggest mental hurdle when learning asyncio. 
Because there is only one thread, 
if any function in that thread blocks 
(like a while True loop, a heavy math calculation, or a synchronous time.sleep()), 
the entire event loop freezes, and no other Tasks can run.
"""