# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright, Playwright
import ddddocr

url = 'https://kyfw.12306.cn/otn/resources/login.html'
res_url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E6%B7%B1%E5%9C%B3%E5%8C%97,IOQ&ts=%E5%B9%BF%E5%B7%9E%E5%8D%97,IZQ&date=2023-03-11&flag=N,Y,Y'


def login_12306(page: Page, username, password):
    uname_xpath = '//*[@id="J-userName"]'
    psw_xpath = '//*[@id="J-password"]'
    page.goto(url)
    page.wait_for_timeout(1000)
    print(page.title())
    page.locator(uname_xpath).fill(username)
    page.locator(psw_xpath).fill(password)
    page.wait_for_timeout(1000)
    page.click('//*[@id="J-login"]')
    page.wait_for_timeout(5000)
    page.click('//*[@id="verification"]/li[1]/a')
    slice_btn = page.locator('//*[@id="nc_1_n1z"]')
    box = slice_btn.bounding_box()
    mid_loc_x = box['x'] + box['width'] / 2
    mid_loc_y = box['y'] + box['height'] / 2
    page.mouse.move(mid_loc_x, mid_loc_y)
    page.mouse.down()
    page.mouse.move(mid_loc_x + 300, mid_loc_y)
    page.wait_for_timeout(1000)
    page.mouse.up()
    page.wait_for_timeout(1000)
    print(page.title())

    return page


def search_ticket(page: Page, from_station, to_station, date):
    search_url = f'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={from_station},IOQ&ts={to_station},IZQ&date={date}&flag=N,Y,Y'
    page.goto(search_url)
    page.wait_for_timeout(5000)

    page.click(f'//*[@id="cc_from_station_{from_station}_check"]')
    page.click(f'//*[@id="cc_to_station_{to_station}_check"]')
    page.wait_for_timeout(6000)
    cur_html = page.content()
    res = BeautifulSoup(cur_html, 'lxml').find('tbody', {'id': 'queryLeftTable'})
    res = res.find_all('tr') if res else []
    print(res)
    print(len(res))


if __name__ == '__main__':
    with sync_playwright() as sp:
        browser = sp.firefox.launch(headless=False, chromium_sandbox=False)
        context = browser.new_context()
        page = context.new_page()
        # page = login_12306(page,
        #                    username='xxx',
        #                    password='xxx')
        search_ticket(page, '深圳北', '广州南', '2023-03-17')
        context.close()
        browser.close()
