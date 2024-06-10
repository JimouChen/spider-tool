# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
from pyhandytools.file import FileUtils


def cal_q_and_w(
        win_num: int,
        lose_num: int,
        tie_good_num: int,
        tie_bad_num: int
):
    tie_num = tie_bad_num + tie_good_num
    q_score = (win_num + tie_num) / (lose_num + tie_num)
    w_score = (win_num + tie_good_num) / (lose_num + tie_good_num)
    return q_score, w_score


def cal_final_score(json_path: str):
    data = FileUtils.load_json(json_path)
    level2res_num_map = {}
    for item in data:
        level_names = item.get('level_names')
        level_key_str = f'{level_names[0]["name"]}:{level_names[1]["name"]}:{level_names[2]["name"]}'
        if level_key_str not in level2res_num_map:
            level2res_num_map[level_key_str] = {
                'win': 0,
                'lose': 0,
                'tie_good': 0,
                'tie_bad': 0
            }
        level2res_num_map[level_key_str][item.get('pred')] += 1
    key_length = len(level2res_num_map)
    avg_weight = 1 / key_length
    final_q_score, final_w_score = 0, 0

    for k, v in level2res_num_map.items():
        q_score, w_score = cal_q_and_w(v.get('win'), v.get('lose'), v.get('tie_good'), v.get('tie_bad'))
        level2res_num_map[k]['q_score'], level2res_num_map[k]['w_score'] = q_score, w_score

        if q_score == -1:
            final_q_score = -1
        if w_score == -1:
            final_w_score = -1

        if (final_q_score == -1) and (final_w_score == -1):
            break

        if final_q_score != -1:
            final_q_score += q_score * avg_weight
        if final_w_score != -1:
            final_w_score += w_score * avg_weight

    print(FileUtils.pretty_json(level2res_num_map))
    print(final_q_score, final_w_score)
    return {
        'level2res_num_map': level2res_num_map,
        'final_q_score': final_q_score,
        'final_w_score': final_w_score
    }


if __name__ == '__main__':
    res = cal_final_score('./data/res.json')
    print(FileUtils.pretty_json(res))
