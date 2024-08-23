# !usr/bin/env python3
# -*- coding:utf-8 -*-
import asyncio
import time

import aiohttp
from loguru import logger


class ApiUtil:
    headers = {'Content-Type': "application/json"}

    @classmethod
    async def post(
            cls, url: str,
            payload: dict = None,
            headers=None,
            verify: bool = False,
            proxy: dict = None,
            timeout=None
    ):

        if headers is None:
            headers = cls.headers
        try:
            timeout = aiohttp.ClientTimeout(total=timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers=headers, ssl=verify, proxy=proxy) as resp:
                    logger.info(
                        f'{url},headers={headers},payload={payload},response：{await resp.json() if resp else resp}')
                    return await resp.json()
        except Exception as e:
            logger.error(f'{url},err：{e},headers={headers},payload={payload}')
            return {}


async def send_request(data, semaphore=asyncio.Semaphore(20)):
    url = 'http://127.0.0.1:1234/llm/mock2'
    async with semaphore:
        resp = await ApiUtil.post(url, payload=data)
        logger.debug(f"{time.time()}---{resp}")
        return resp


async def main():
    data_list = [
        {'prompt': f'7777_{_}', 'msg_id': _} for _ in range(60)
    ]

    tasks = [send_request(data) for data in data_list]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        print(response)

# 推荐
async def main_():
    data_list = [
        {'prompt': f'7777_{_}', 'msg_id': _} for _ in range(60)
    ]

    semaphore = asyncio.Semaphore(80)  # 限制并发量为20
    tasks = [send_request(data, semaphore) for data in data_list]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        # handle the response
        print(response)


if __name__ == '__main__':
    asyncio.run(main_())
