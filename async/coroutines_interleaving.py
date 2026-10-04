import asyncio
import time

async def worker(name, delay, steps):
    print(f"[{time.strftime('%X')}] Task {name}: Started")
    
    for i in range(steps):
        print(f"[{time.strftime('%X')}] Task {name}: Working on step {i+1}/{steps}...")
        
        # --- THE YIELD POINT ---
        # asyncio.sleep(delay) returns a Future that resolves in 'delay' seconds.
        # By awaiting it, we yield the main thread back to the event loop.
        await asyncio.sleep(delay)
        
    print(f"[{time.strftime('%X')}] Task {name}: Finished")
    return f"Result of {name}"

# 1. Setup the loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 2. Create the coroutines
coro_a = worker("A", delay=1.0, steps=3)
coro_b = worker("B", delay=1.5, steps=2)

# 3. Schedule them as Tasks. 
# This immediately puts Task._step for both into the loop's call_soon queue.
task_a = loop.create_task(coro_a)
task_b = loop.create_task(coro_b)

print("Starting loop. Watch the timestamps closely!")

# 4. We need the loop to run until BOTH tasks are done.
# asyncio.gather wraps multiple awaitables into a single Future.
combined_future = asyncio.gather(task_a, task_b)

# Run the loop until the combined_future is FINISHED
results = loop.run_until_complete(combined_future)

print(f"All tasks completed. Results: {results}")
loop.close()