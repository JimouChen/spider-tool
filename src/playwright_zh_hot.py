# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright, Playwright

aim_url = 'xxx'
js_scroll = "var q=document.documentElement.scrollTop=10000"


def crawl(page: Page, url):
    page.goto(url)
    page.wait_for_timeout(1000)
    page.click('//html/body/div[5]/div/div/div/div[2]/button')
    page.wait_for_timeout(4000)
    print(page.title())
    # 向下滑动
    for _ in range(4):
        page.evaluate(js_scroll)
        page.wait_for_timeout(2000)
    sleep(2)

    cur_html = page.content()
    soup = BeautifulSoup(cur_html, 'lxml')
    items = soup.find_all('div', {'class', 'List-item TopicFeedItem'})
    print(len(items))
    for idx, item in enumerate(items):
        title = item.find('h2', {'class': 'ContentItem-title'}).text
        print('title: ', title)
        # answer = ''
        if '阅读全文' in str(item):
            # read_more_xpath = '//*[@id="TopicMain"]/div[3]/div/div/div/div[2]/div/div/div/div[2]/span/div/button'
            read_more_xpath = f'//*[@id="TopicMain"]/div[3]/div/div/div/div[{idx + 2}]/div/div/div/div[2]/span/div/button'
            page.click(read_more_xpath)
            page.wait_for_timeout(1000)
            cur_html = page.content()
            answer = BeautifulSoup(cur_html, 'lxml').find_all('span', {
                'class': 'RichText ztext CopyrightRichText-richText css-1g0fqss'})[idx].text
        else:
            answer = item.find('div', {'class': 'css-376mun'}).text
        print('answer:', answer)

    return page


if __name__ == '__main__':
    with sync_playwright() as sp:
        browser = sp.firefox.launch(headless=False,
                                    chromium_sandbox=False)
        context = browser.new_context()
        page = context.new_page()
        page = crawl(page, aim_url)

        context.close()
        browser.close()
