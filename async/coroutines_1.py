import asyncio
from inspect import isgenerator
from asyncio import Future
from typing import Awaitable, Iterable, Generator

async def test_coroutine(future: Future):
    print("[Coro] Started running...")
    print("[Coro] Hitting await. Pausing and yielding the Future to the caller.")

    print(f"Future is awaitable? Well {isinstance(future, Awaitable)}")
    print(f"Future is iterable? Well {isinstance(future, Iterable)}")
    print(f"Future is generator? Well {isgenerator(future)}")
    
    # 'await' yields the future outward, and pauses the function here.
    # When the function is resumed, it extracts the result of the future.
    result = await future
    
    print(f"[Coro] Resumed! The future contained: {result}")
    return "Final Coroutine Value"

# 1. Create our building blocks
loop = asyncio.new_event_loop()
my_future = loop.create_future()

# 2. Instantiate the coroutine (nothing executes yet)
coro = test_coroutine(my_future)
print(f"[Main] Created coroutine object: {coro}")
print(f"Coroutine is generator? Well {isgenerator(coro)}")

# 3. Manually step the coroutine forward using .send(None)
# This runs the coro until it hits 'await my_future', which yields my_future back to us.
yielded_future: Future = coro.send(None)
print(f"[Main] The coroutine yielded: {yielded_future._state}")

# 4. Resolve the future
print("[Main] Resolving the future...")
my_future.set_result("Hello from the outside!")

# 5. Step the coroutine forward again. 
# Because the future is resolved, the coroutine will finish and raise StopIteration.
try:
    # In raw Python, we pass the data back in via .send() or rely on the 
    # coroutine to call future.result() when it unpauses.
    # coro.send(None)
    pass 
except StopIteration as e:
    print(f"[Main] Coroutine finished. Return value was: {e.value}")

loop.close()

# -----------------------------------------------------

"""
my_future.set_result("Hello from the outside!") does exactly two things:

 1. It changes the Future's internal state from PENDING to FINISHED.

 2. It stores the string "Hello from the outside!" inside the Future.

Crucially, it does not unpause the coroutine.

Because we are manually driving the coroutine without a running event loop, 
set_result just passively updates the Future's state. 
The coroutine remains frozen at the await line until we manually push it forward again by calling coro.send(None). 
When we do, the coroutine wakes up, inspects the Future, sees it is FINISHED, 
calls my_future.result() to extract the string, and continues executing.
"""