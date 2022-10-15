"""
爬取leetcode剑指Offer2的题目和链接，并存为md文件
输出格式上可能有个别文件有点儿瑕疵，但是思路没问题
"""
import requests
import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)

save_md_root = './md_file/'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Connection': 'keep-alive'
}


def get_context():
    url1 = 'https://leetcode.cn/problem-list/xb9nqhhg/'
    next_page_url = 'https://leetcode.cn/problem-list/xb9nqhhg/?page=2'
    base_url = 'https://leetcode.cn'
    first_page = requests.get(url=url1, headers=header).text
    second_page = requests.get(url=next_page_url, headers=header).text
    # main_page = BeautifulSoup(url1, 'html.parser').find_all(attrs={'div': 'truncate overflow-hidden'})
    problem_link = re.findall('/problems/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                              first_page + second_page)

    problems = [base_url + link for idx, link in enumerate(problem_link) if idx % 2 == 0]

    for idx, problem_url in enumerate(problems):
        print(problem_url)
        driver.get(problem_url)
        driver.implicitly_wait(2)
        # 太快的话爬不到
        sleep(1)
        e = driver.find_element('class name', 'notranslate').text
        title, desc = parse_str(e)
        md_title = '[' + title + '](' + problem_url + ')\n\n'
        desc = '> ' + desc
        write_to_md(save_md_root + title + '.md', md_title + desc)
    driver.close()


def parse_str(text: str):
    start, end = 0, 0
    for idx, t in enumerate(text):
        if text[idx: idx + 4] == '提交记录':
            start = idx + 4
        if text[idx: idx + 4] == '通过次数':
            end = idx
            break
    text = text[start: end]
    title = text[1:text.index('难度\n') - 2]
    print(title)
    return title, text


def write_to_md(md_path, text):
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('finished')


if __name__ == '__main__':
    get_context()
