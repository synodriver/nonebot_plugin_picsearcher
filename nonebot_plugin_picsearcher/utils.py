# -*- coding: utf-8 -*-
from typing import AsyncGenerator


async def limiter(gen: AsyncGenerator, limit: int):
    num = 0
    try:
        while num < limit:
            yield await gen.asend(None)
            num += 1
    except StopAsyncIteration:
        pass


if __name__ == "__main__":
    import asyncio


    async def test():
        for i in range(10):
            yield i


    async def main():
        async for i in limiter(test(), 5):
            print(i)


    asyncio.run(main())
