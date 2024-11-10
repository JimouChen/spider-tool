import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait

from pyhandytools.file import FileUtils
from loguru import logger

json_data = FileUtils.load_json('./data/case_set/prompts_.json')
file_lock = threading.Lock()


def process_dialogue(case_id):
    for item in json_data[case_id]:
        msg_id = item.get('msg_id')
        time.sleep(2)
        # mock llm infer
        logger.debug(f"{case_id=}, {msg_id=}")
        item["answer"] = f"answer_{case_id}_{msg_id}"

    with file_lock:
        FileUtils.write2json('./data/case_set/prompts_.json', json_data)
        logger.debug(f"Thread {threading.current_thread().name} has updated the file for round {case_id}.")


if __name__ == '__main__':
    try:
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for key in json_data.keys():
                future = executor.submit(process_dialogue, key)
                futures.append(future)

            wait(futures)
        logger.info("All threads have finished processing and the JSON file has been updated.")
    except KeyboardInterrupt as e:
        logger.error(f'KeyboardInterrupt {e}')
        logger.info('close... wait 3s.')
        for i in range(3):
            time.sleep(1)
            logger.debug(f'waiting {i+1}s...')
    finally:
        pass

