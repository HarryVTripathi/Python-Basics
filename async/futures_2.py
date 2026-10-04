import asyncio
from asyncio import Future

def on_future_done(fut: Future):
    # This function automatically receives the Future object as its argument
    print(f"Callback fired! Future is done. {type(fut)} and {isinstance(fut, Future)}")
    
    try:
        # fut.result() will either return the data or raise the stored exception
        data = fut.result()
        print(f"The result was: {data}")
    except Exception as e:
        print(f"The future failed with: {e}")
        
    # Stop the loop now that our work is done
    loop.stop()

# 1. Setup the loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 2. Create the Future
fetch_data_future = loop.create_future()

# 3. Attach our callback to the Future
fetch_data_future.add_done_callback(on_future_done)

# 4. Schedule the Future to resolve in 1 second
# We are essentially doing: loop.call_later(1.0, my_future.set_result, "Network Data")
loop.call_later(1.0, fetch_data_future.set_result, "Successfully fetched data!")

# Alternatively, to simulate a failure, you would use:
# loop.call_later(1.0, my_future.set_exception, ValueError("Network timeout!"))

print("Starting the loop. Waiting for the Future to resolve...")
loop.run_forever()
loop.close()
