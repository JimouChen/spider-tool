# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright, Playwright

aim_url = ['https://www.allhistory.com/relation?networkId=5cc51d4c3ae20d0001cee0b3',
           'https://www.allhistory.com/relation?networkId=5cfd48493ae20d000199da4f']
js_scroll = "var q=document.documentElement.scrollTop=100000"

class BrowserController:
    @staticmethod
    def load(sp: Playwright):
        browser = sp.chromium.launch(headless=True,
                                     chromium_sandbox=False)
        context = browser.new_context()
        page = context.new_page()

        return browser, context, page

    @staticmethod
    def clear(browser, context):
        context.close()
        browser.close()

def crawl(page: Page, url):
    page.goto(url)
    page.wait_for_timeout(1000)
    print(page.title())
    # xpath定位不到的情况可以用选择器来定位
    # know_xpath = '//html/body/div[14]/div'
    know_slt = 'body > div.dls-cookie-banner > div'
    # if page.locator(know_xpath):
    #     page.click(know_xpath)
    if page.query_selector(know_slt):
        page.click(know_slt)

    page.wait_for_timeout(1000)
    list_xpath = '//*[@id="relationlist-container"]/div/ul/li'
    page.click(list_xpath)
    page.wait_for_timeout(4000)
    cur_html = page.content()
    li_list = BeautifulSoup(cur_html, 'lxml').find_all('li')
    print(len(li_list))
    for li in li_list:
        print('context: ', end='')
        print(li.text.replace(' ', '').replace('\n', ''))
        print()
    return page


if __name__ == '__main__':
    with sync_playwright() as sp:
        browser, context, page = BrowserController.load(sp)
        for url in aim_url:
            page = crawl(page, url)

        BrowserController.clear(browser, context)
