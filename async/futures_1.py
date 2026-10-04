"""
The Mechanics of What Just Happened

 1. `loop.create_future()`: You created an empty box. 

At this stage, calling my_future.result() would crash the program with an InvalidStateError because the box is empty.

 2. `my_future.add_done_callback()`: You attached a tripwire to the box. 
 
You told the event loop, "The moment something is placed in this box, run this function."

 3. `fut.set_result(value)`: Inside the worker function, you placed the string "Phase 2 Mastered" into the box. 
 
This immediately changes the Future's state to "Done".

 4. The Trigger: The instant the Future becomes "Done", two things happen simultaneously:

   - The loop fires the `on_future_done` callback, allowing it to print the result.

   - The `run_until_complete()` method detects the state change, captures the result, 
  triggers `loop.stop()` internally, and returns the result back to your main script.
"""


import asyncio
import time
from asyncio import Future

# 1. Instantiate the engine
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 2. Create a blank Future
# This creates a "Pending" placeholder attached to our specific loop.
my_future = loop.create_future()

# 3. Define a callback to react when the Future is done
def on_future_done(fut: Future):
    # fut is automatically passed to the callback
    print(f"[{time.strftime('%X')}] Callback: The Future is done! Value: {fut.result()}")

# Attach the reaction to the Future
my_future.add_done_callback(on_future_done)


# 4. Define the worker function that will eventually produce the result
def resolve_the_future(fut, value):
    print(f"[{time.strftime('%X')}] Worker: Resolving the Future now...")
    fut.set_result(value)

# 5. Schedule the worker on the conveyor belt
# We schedule it to run 3 seconds from now.
print(f"[{time.strftime('%X')}] Scheduling the worker 3 seconds into the future...")
loop.call_later(3.0, resolve_the_future, my_future, "Phase 2 Mastered")

# 6. Run the engine using the Future
print(f"[{time.strftime('%X')}] Engine starting with run_until_complete()...")

# The loop will block here, process I/O and time delays, and automatically
# stop the exact millisecond my_future.set_result() is called.
final_result = loop.run_until_complete(my_future)

print(f"[{time.strftime('%X')}] Engine stopped. run_until_complete returned: {final_result}")

loop.close()
