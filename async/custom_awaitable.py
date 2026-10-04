import asyncio

class CustomAwaitable:
    def __init__(self, delay, message):
        self.delay = delay
        self.message = message

    def __await__(self):
        # We yield a Future to the event loop and wait for it to resolve.
        # This is EXACTLY what `await asyncio.sleep()` does natively.
        yield from asyncio.sleep(self.delay).__await__()
        return self.message

# You can now 'await' this standard class as if it were a coroutine
async def main():
    obj = CustomAwaitable(1, "Built from scratch!")
    result = await obj 
    print(result)
