# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import asyncio
import time


async def work(name: str):
    print(name + ' start')
    await asyncio.sleep(1)
    print(name + ' done')


async def main():
    start = time.time()
    todo = ['111', '222', '333']
    tasks = [work(item) for item in todo]
    res = await asyncio.gather(*tasks, return_exceptions=True)
    print(res)
    print(time.time() - start)


if __name__ == '__main__':
    asyncio.run(main())
"""
任务中要有sleep才可以进行asyncio异步加速，
否则效果和串行执行差距不大，甚至变慢了
"""
