# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import re
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright, Playwright
from utils import *

aim_url = 'https://www.allhistory.com/book/home-list'
js_scroll = "var q=document.documentElement.scrollTop=100000"


def crawl(page: Page, url):
    page.goto(url)
    page.wait_for_timeout(1000)
    print(page.title())
    read_more_xpath = '//*[@id="app-container"]/div[1]/ul/li[4]/div[3]/div[2]'
    page.click(read_more_xpath)
    page.wait_for_timeout(3000)
    all_title_list = set()

    selector = 'body > div.book-list-home-pop.pop-box-mask.scroll-box--wrapped.scroll-box--show-axis-y.ps.ps--active-y.ps--focus.ps--active-x > div.pop-content > div.page-right'
    i = 0
    while page.locator(selector).is_visible():
        # if i % 6 == 0 or not page.locator(selector).is_visible():
        cur_html = page.content()
        cur_title_list = BeautifulSoup(cur_html, 'lxml') \
            .find('div', {'class': 'swiper-wrapper'}) \
            .find_all('div', {'class': 'normal-title'})
        for title in cur_title_list:
            all_title_list.add(title.text.replace(' ', '').replace('\n', ''))
        page.click(selector)
        page.wait_for_timeout(100)
        i += 1

    print(all_title_list)
    print(len(all_title_list))

    return page


if __name__ == '__main__':
    with sync_playwright() as sp:
        browser, context, page = BrowserController.load(sp)
        page = crawl(page, aim_url)

        BrowserController.clear(browser, context)
