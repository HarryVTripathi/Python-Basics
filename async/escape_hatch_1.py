import asyncio
import time
import concurrent.futures

# 1. A standard, blocking synchronous function
# Notice there is no 'async' here. This function uses time.sleep().
# If we ran this directly on the event loop, it would freeze the entire program.
def blocking_legacy_code(task_id):
    print(f"[{time.strftime('%X')}] Thread {task_id}: Starting 2-second blocking work...")
    time.sleep(2.0) 
    print(f"[{time.strftime('%X')}] Thread {task_id}: Unblocked!")
    return f"Data from Thread {task_id}"

# 2. A native async coroutine to prove the engine is still alive
async def native_async_watcher():
    print(f"[{time.strftime('%X')}] Watcher: Started.")
    for i in range(5):
        print(f"[{time.strftime('%X')}] Watcher: Event loop is freely ticking... ({i+1}/5)")
        await asyncio.sleep(0.5)

# --- Engine Setup ---
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 3. Create a standard Python ThreadPool
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

print(f"[{time.strftime('%X')}] Engine starting. Dispatching work to threads...")

# 4. The Bridge: run_in_executor
# We tell the engine: "Send this function to a background thread. 
# Give me a Future NOW, and resolve it when the thread is done."
future_a = loop.run_in_executor(executor, blocking_legacy_code, "A")
future_b = loop.run_in_executor(executor, blocking_legacy_code, "B")

# Schedule our async watcher to run concurrently on the main loop
watcher_task = loop.create_task(native_async_watcher())

# Group our threaded Futures and our native Task together
master_future = asyncio.gather(future_a, future_b, watcher_task)

# Run the engine until the threads and the watcher are all finished
results = loop.run_until_complete(master_future)

print(f"[{time.strftime('%X')}] Engine stopped.")
# results[0] and [1] are from the threads, results[2] is None from the watcher
print(f"Final Thread Results: {results[:2]}")

loop.close()
