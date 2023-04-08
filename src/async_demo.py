# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import asyncio
import time


async def work1():
    i = 0
    await asyncio.sleep(0.1)
    for _ in range(20000000):
        i += 1


async def work2():
    i = 0
    await asyncio.sleep(0.1)
    for _ in range(20000000):
        i += 1


def work3():
    i = 0
    time.sleep(0.1)
    for _ in range(20000000):
        i += 1


def main1():
    start = time.time()
    work3()
    work3()
    work3()
    print(time.time() - start)


async def main():
    start = time.time()
    tasks = [work1(), work1(), work2()]
    res = await asyncio.gather(*tasks, return_exceptions=True)
    print(res)
    print(time.time() - start)


if __name__ == '__main__':
    asyncio.run(main()) # 2.752410888671875
    # main1() # 3.00
