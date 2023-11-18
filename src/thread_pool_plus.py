from concurrent.futures import ThreadPoolExecutor, wait
import time
import threading

from pyhandytools.file import FileUtils
from loguru import logger

"""
外部模型粒度+内部用例粒度+可控制并发数请求llm的算法
避免频繁地创建和销毁线程，提速的同时，节省资源；
"""

pool = ThreadPoolExecutor()
max_worker_num = 2


def get_res(s: str):
    time.sleep(1)
    return s + '_ans'


def sort_and_show(name: str, res: list):
    res = sorted(res, key=lambda x: x['idx'])
    FileUtils.write2json(f'./data/{name}_ans.json', res)
    logger.success(f'{name} finished!')
    logger.info(f'res: {res}')


def llm_req(name: str, prompts: list):
    """
    可以控制for内的线程并发数量，通过线程池控制
    业务逻辑全封装到worker中
    """
    res = []

    def worker(_: dict):
        # 针对multi turn，这里内部直接取出caseId，内部按turn顺序请求llm即可
        mid = _.get('mid')
        prompt = _.get('prompt')
        ans = name + '_' + get_res(prompt)
        logger.info(f'mid: {mid} ==> {ans}')
        return {
            'idx': _.get('idx'),
            'mid': mid,
            'ans': ans
        }

    with ThreadPoolExecutor(max_workers=max_worker_num) as executor:
        futures = [executor.submit(worker, item) for item in prompts]
        for future in futures:  # 遍历future对象的列表
            res.append(future.result())  # 获取每个future对象的结果，并添加到res列表中
    sort_and_show(name, res)

    return res


def llm_req__(name: str, prompts: list):
    """
    for 内使用系统所有并发
    - 缺点：
    系统自身没有那么多的线程，可能会遇到一些问题：
    比如，程序可能会消耗过多的内存和CPU资源，导致系统变慢或者崩溃；
    或者，程序可能会受到操作系统的线程限制，导致无法创建更多的线程，抛出异常；
    - 优点
    少量数据时，可充分发挥系统性能
    
    """
    res = []
    threads = []

    def worker(_: dict):
        mid = _.get('mid')
        prompt = _.get('prompt')
        ans = name + '_' + get_res(prompt)
        res.append({
            'idx': _.get('idx'),
            'mid': mid,
            'ans': ans
        })
        logger.info(f'mid: {mid} ==> {ans}')

    for idx, item in enumerate(prompts):
        item['idx'] = idx
        t = threading.Thread(target=worker, args=(item,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    # sort res
    sort_and_show(name, res)


def llm_req_(name: str, prompts: list):
    res = []
    for item in prompts:
        mid = item.get('mid')
        prompt = item.get('prompt')
        ans = name + '_' + get_res(prompt)
        res.append({
            'mid': mid,
            'ans': ans
        })
        logger.info(f'mid: {mid} ==> {ans}')
    FileUtils.write2json(f'./data/{name}_ans.json', res)
    logger.success(f'{name} finished!')
    logger.info(f'res: {res}')


def gel_llm_res(data: dict):
    # 外部采用线程池
    prompt_list = data.get('prompt_list')
    start = time.time()
    features = [
        pool.submit(llm_req, 'llm_a', prompt_list),
        pool.submit(llm_req, 'llm_b', prompt_list),
        pool.submit(llm_req, 'llm_c', prompt_list),
    ]
    wait(features)
    pool.shutdown()
    logger.info('finished!')
    logger.info(f'cost: {time.time() - start} s')


def gel_llm_res2(data: dict):
    prompt_list = data.get('prompt_list')
    start = time.time()
    llm_req('llm_a', prompt_list)
    llm_req('llm_b', prompt_list)
    llm_req('llm_c', prompt_list)
    logger.info('finished!')
    logger.info(f'cost: {time.time() - start} s')


if __name__ == '__main__':
    # gel_llm_res2({
    gel_llm_res({
        'prompt_list': [
            {'mid': 1, 'prompt': 'q1'},
            {'mid': 2, 'prompt': 'q2'},
            {'mid': 3, 'prompt': 'q3'},
        ]
    })
