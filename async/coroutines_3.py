import asyncio
import time

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 1. Define a finite coroutine that actually returns a value
async def fetch_data(task_id, delay):
    print(f"[{time.strftime('%X')}] Task {task_id}: Fetching data... (takes {delay}s)")
    
    # Yield control back to the loop while waiting
    await asyncio.sleep(delay)
    
    print(f"[{time.strftime('%X')}] Task {task_id}: Data retrieved!")
    # Returning a value automatically sets the result of the underlying Task (Future)
    return f"Payload from {task_id}"

# 2. Wrap the coroutines in Tasks and schedule them
task1 = loop.create_task(fetch_data("A", 1.5))
task2 = loop.create_task(fetch_data("B", 2.0))
task3 = loop.create_task(fetch_data("C", 1.0))

print(f"[{time.strftime('%X')}] Engine starting. Waiting for all tasks to succeed...")

# 3. Use asyncio.gather to combine multiple Tasks into a single master Future.
# The loop will run until this master Future is Done (which happens when all 3 finish).
master_future = asyncio.gather(task1, task2, task3)
results = loop.run_until_complete(master_future)

print(f"[{time.strftime('%X')}] Engine stopped naturally.")
print(f"Final Results: {results}")

loop.close()
