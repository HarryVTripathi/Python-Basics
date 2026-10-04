import asyncio
import time
from asyncio import Task


# 1. Instantiate the engine
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 2. Define an asynchronous worker
async def worker(name, delay):
    print(f"[{time.strftime('%X')}] {name}: Started")
    try:
        while True:
            # 'await' suspends this function and yields control back to the event loop.
            # asyncio.sleep under the hood creates a Future and uses call_later to resolve it.
            await asyncio.sleep(delay)
            print(f"[{time.strftime('%X')}] {name}: Completed a work cycle")
    except asyncio.CancelledError:
        # This exception is magically injected into the coroutine AT the 'await' line.
        print(f"[{time.strftime('%X')}] {name}: Received cancellation signal! Cleaning up...")

# 3. Create Tasks (wrapping the coroutines) and put them on the loop
# This does not run them immediately; it just schedules them for the next loop iteration.
task1 = loop.create_task(worker("Worker A", 1.0))
task2 = loop.create_task(worker("Worker B", 1.5))
task3 = loop.create_task(worker("Worker C", 2.0))

# 4. Let the engine run for 5 seconds
print(f"[{time.strftime('%X')}] Engine running for 5 seconds...")
# We can use asyncio.sleep(5) as a dummy Future to keep the loop alive for exactly 5 seconds
loop.run_until_complete(asyncio.sleep(5.0))

# 5. The Graceful Shutdown Mechanics
print(f"[{time.strftime('%X')}] 5 seconds reached. Initiating shutdown sequence...")

# asyncio.all_tasks() retrieves every Task currently registered on this loop
pending_tasks = asyncio.all_tasks(loop)

for task in pending_tasks:
    print(f"[{time.strftime('%X')}] Cancelling {task.get_coro().__name__}...")
    task.cancel()  # Flags the task for cancellation

# 6. Flush the engine
# Calling .cancel() merely schedules the CancelledError to be raised. 
# We MUST run the loop one last time so the engine can actually throw the exceptions 
# into the coroutines, allowing their 'except' blocks to execute.
print(f"[{time.strftime('%X')}] Flushing engine to process cleanups...")
# We use gather to run the loop until all tasks finish their cleanup
loop.run_until_complete(asyncio.gather(*pending_tasks, return_exceptions=True))

print(f"[{time.strftime('%X')}] All tasks destroyed. Closing engine.")
loop.close()
