from concurrent.futures import ThreadPoolExecutor, wait
import time

pool = ThreadPoolExecutor()


def write2db(res: list):
    time.sleep(2)
    print('write ok:', res)


def llm_a(prompt: list[str]):
    time.sleep(1)
    res = ['ans a ' + p for p in prompt]
    print('llm_a: ', res)
    write2db(res)


def llm_b(prompt: list[str]):
    time.sleep(1)
    res = ['ans b ' + p for p in prompt]
    print('llm_b: ', res)
    write2db(res)


def llm_c(prompt: list[str]):
    time.sleep(1)
    res = ['ans c ' + p for p in prompt]
    print('llm_c: ', res)
    write2db(res)


def gel_llm_res(data: dict):
    prompt_list = data.get('prompt_list')
    start = time.time()
    features = [
        pool.submit(llm_a, prompt_list),
        pool.submit(llm_b, prompt_list),
        pool.submit(llm_c, prompt_list)
    ]
    wait(features)
    pool.shutdown()
    print('finished!')
    print(f'cost: {time.time() - start} s')


def gel_llm_res2(data: dict):
    prompt_list = data.get('prompt_list')
    start = time.time()
    llm_a(prompt_list)
    llm_b(prompt_list)
    llm_c(prompt_list)
    print('finished!')
    print(f'cost: {time.time() - start} s')


if __name__ == '__main__':
    gel_llm_res({
        'prompt_list': ['q1', 'q2', 'q3', 'q4']
    })
    #
    # gel_llm_res2({
    #     'prompt_list': ['q1', 'q2', 'q3', 'q4']
    # })
