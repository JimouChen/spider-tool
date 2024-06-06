# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

from pyhandytools.file import FileUtils


def check_split_multi_tune(file_pre_path: str, n):
    if n == 1:
        return
    all_data = [FileUtils.load_json(f'{file_pre_path}_{i}.json') for i in range(1, n + 1)]
    i = 0
    while i < n - 1:
        cur_data, next_data = all_data[i], all_data[i + 1]
        if next_data[0].get('msg_id') != 1:
            for item in next_data:
                if item.get('msg_id') != 1:
                    cur_data.append(item)
                    next_data = next_data[1:]
                else:
                    break
        all_data[i], all_data[i + 1] = cur_data, next_data
        i += 1
    for idx, item in enumerate(all_data):
        FileUtils.write2json(f'{file_pre_path}_{idx + 1}.json', item)


if __name__ == '__main__':
    check_split_multi_tune('./data/a', n=4)
