import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait

from pyhandytools.file import FileUtils
from loguru import logger

json_data = FileUtils.load_json('./data/case_set/prompts_.json')
file_lock = threading.Lock()


def process_dialogue(round_key):
    for item in json_data[round_key]:
        # time.sleep(1)
        # mock llm infer
        item["answer"] = f"answer_{round_key}_{item.get('msg_id')}"

    with file_lock:
        FileUtils.write2json('./data/case_set/prompts_.json', json_data)
        logger.debug(f"Thread {threading.current_thread().name} has updated the file for round {round_key}.")


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for key in json_data.keys():
            future = executor.submit(process_dialogue, key)
            futures.append(future)

        wait(futures)
    logger.info("All threads have finished processing and the JSON file has been updated.")
