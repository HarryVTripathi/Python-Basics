import asyncio
import time

# 1. Manually instantiate the engine
# By default, high-level asyncio creates this for you. We are building it by hand.
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 2. Define standard, synchronous callback functions
# Notice there is no 'async def' here. These are normal functions.
def task_a():
    print(f"[{time.strftime('%X')}] Task A: Executed immediately")

def task_b(delay):
    print(f"[{time.strftime('%X')}] Task B: Executed after {delay} seconds")

def task_c():
    print(f"[{time.strftime('%X')}] Task C: Executed at an absolute timestamp")

def stop_engine(loop):
    print(f"[{time.strftime('%X')}] Halting the event loop...")
    loop.stop()

print(f"[{time.strftime('%X')}] Engine starting...")

# 3. Schedule the tasks on the conveyor belt

# call_soon schedules the function for the very next iteration of the loop.
loop.call_soon(task_a)

# call_later schedules the function based on a relative time delay.
loop.call_later(2.0, task_b, 2.0)

# call_at schedules based on the loop's internal monotonic clock (NOT time.time()).
current_loop_time = loop.time()
loop.call_at(current_loop_time + 3.5, task_c)

# Schedule our kill switch to fire after 5 seconds
loop.call_later(5.0, stop_engine, loop)

# 4. Turn the engine on
# This function will block the main thread infinitely until loop.stop() is called.
try:
    loop.run_forever()
finally:
    # Always clean up the engine to prevent memory leaks
    print("Closing the engine.")
    loop.close()
